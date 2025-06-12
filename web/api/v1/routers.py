import pandas as pd
import logging
import io
import math
import asyncio
from typing import AsyncGenerator
from dataclasses import asdict
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse

from manager.product_manager import EbayProductManager
from manager.product_translate import ProductTranslateManager
from manager.currency_manager import CurrencyManager
from services.processors.file_processor import FileProcessor
from services.task_tracker import task_tracker
from fastapi.encoders import jsonable_encoder
import httpx


router = APIRouter(prefix="/api")
product_manager = EbayProductManager()
translate_manager = ProductTranslateManager()
currency_manager = CurrencyManager()
file_processor = FileProcessor()


@router.get("/")
async def root():
    return {"message": "Hello World"}


async def process_search_task(task_id: str, query: str, category: str = None):
    """Background task to process search request."""
    try:
        # Update task to processing state immediately
        task_tracker.update_task(
            task_id, 
            "processing", 
            progress={"processed": 0, "total": 0, "status": "fetching_products"}
        )
        
        # Run product search
        products = await product_manager.search_products(query=query, category=category)
        
        total_count = len(products) if products else 0
        task_tracker.update_task(
            task_id,
            "processing",
            progress={
                "processed": 0,
                "total": total_count,
                "status": "processing_products"
            }
        )
        
        # Process products in smaller batches
        batch_size = 10
        processed_count = 0
        total_products = []
        
        for i in range(0, total_count, batch_size):
            batch = products[i:i + batch_size]
            
            # Process batch
            processed_batch = [
                {**p, 'product_details': asdict(p['product_details'])} 
                if 'product_details' in p and p['product_details'] 
                else p 
                for p in batch
            ]
            
            total_products.extend(processed_batch)
            processed_count += len(batch)
            
            # Update task with current progress
            task_tracker.update_task(
                task_id, 
                "processing", 
                result=total_products,
                progress={
                    "processed": processed_count,
                    "total": total_count,
                    "status": "processing_products"
                }
            )
            
            # Allow other tasks to run
            await asyncio.sleep(0.05)
        
        task_tracker.update_task(
            task_id, 
            "completed", 
            result=total_products,
            progress={
                "processed": total_count,
                "total": total_count,
                "status": "completed"
            }
        )
    except Exception as e:
        logging.error(f"Search failed: {str(e)}")
        task_tracker.update_task(
            task_id, 
            "failed", 
            error=str(e),
            progress={"status": "failed"}
        )


async def process_translate_task(task_id: str, file_content: bytes):
    """Background task to process translation request."""
    try:
        df = pd.read_csv(io.StringIO(file_content.decode("utf-8")))
        translated = await translate_manager.translate_product(df)
        result = translated.to_dict("records")
        task_tracker.update_task(task_id, "completed", result=result)
    except Exception as e:
        logging.error(f"Translation failed: {str(e)}")
        task_tracker.update_task(task_id, "failed", error=str(e))


async def process_bundle_task(
    task_id: str,
    file_content: bytes,
    lures_per_bundle: int,
    min_usd_value: float,
    target_yen_per_lure: float
):
    """Background task to process bundle creation request."""
    try:
        df = pd.read_csv(io.BytesIO(file_content))
        bundles = product_manager.generate_bundles(
            df, lures_per_bundle, min_usd_value, target_yen_per_lure
        )
        task_tracker.update_task(task_id, "completed", result=bundles)
    except Exception as e:
        logging.error(f"Bundle creation failed: {str(e)}")
        task_tracker.update_task(task_id, "failed", error=str(e))


async def process_currency_task(
    task_id: str,
    amount: float,
    from_currency: str,
    to_currency: str
):
    """Background task to process currency conversion request."""
    try:
        converted = currency_manager.calculate_price_map(from_currency, amount)
        result = {"convertedAmount": converted.get(to_currency)}
        task_tracker.update_task(task_id, "completed", result=result)
    except Exception as e:
        logging.error(f"Currency conversion failed: {str(e)}")
        task_tracker.update_task(task_id, "failed", error=str(e))


@router.post("/pipeline")
async def run_pipeline(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    lures_per_bundle: int = Form(5),
    min_usd_value: float = Form(50.0),
    target_yen_per_lure: float = Form(1000.0),
):
    """
    Start a background pipeline task and return task ID.
    The task will:
    1. Clean data
    2. Translate product names
    3. Add pricing information
    4. Generate bundles
    """
    task_id = task_tracker.create_task("pipeline")
    task_tracker.update_task(task_id, "pending")
    
    # Read file content
    file_content = await file.read()
    
    # Add the processing task to background tasks
    background_tasks.add_task(
        process_pipeline_task,
        task_id,
        file_content,
        lures_per_bundle,
        min_usd_value,
        target_yen_per_lure
    )
    
    return JSONResponse(
        content={"task_id": task_id, "status": "pending"},
        status_code=202
    )


async def process_pipeline_task(
    task_id: str,
    file_content: bytes,
    lures_per_bundle: int,
    min_usd_value: float,
    target_yen_per_lure: float
):
    """Background task to process pipeline request."""
    try:
        # Read the CSV file
        task_tracker.update_task(task_id, "processing", progress={"step": "reading_file"})
        df = pd.read_csv(io.BytesIO(file_content))

        # clean "Title" column drop nulls
        task_tracker.update_task(task_id, "processing", progress={"step": "cleaning_data"})
        df_cleaned = df[df["Title"].notna()]
        del df

        # 2. Translate Product Names
        task_tracker.update_task(task_id, "processing", progress={"step": "translation"})
        df_translated = await translate_manager.translate_product(df_cleaned)
        del df_cleaned

        if df_translated is None or df_translated.empty:
            raise ValueError("Translation failed or produced empty DataFrame")

        # 3. Search for Product Prices
        task_tracker.update_task(task_id, "processing", progress={"step": "pricing"})
        df = await product_manager.add_pricing_to_dataframe(df_translated)
        del df_translated

        if df is None or df.empty:
            raise ValueError("Pricing failed or produced empty DataFrame")

        # 4. Create Bundles
        task_tracker.update_task(task_id, "processing", progress={"step": "bundling"})
        bundles, leftovers = product_manager.generate_bundles(
            df, lures_per_bundle, min_usd_value, target_yen_per_lure
        )

        if bundles is None:
            raise ValueError("Bundle generation failed")

        # Clean and prepare the response
        task_tracker.update_task(task_id, "processing", progress={"step": "finalizing"})
        
        response_data = {
            "bundles": [
                {
                    "id": bundle.id,
                    "products": [
                        {
                            "title": product.title,
                            "price_usd": product.price_usd,
                            "price_aud": product.price_aud,
                        }
                        for product in bundle.products
                    ],
                    "total_value_usd": bundle.total_value_usd,
                    "total_value_aud": bundle.total_value_aud,
                }
                for bundle in bundles
            ],
            "leftovers": [
                {
                    "title": product.title,
                    "price_usd": product.price_usd,
                    "price_aud": product.price_aud,
                }
                for product in leftovers
            ],
        }

        # save to csv
        task_tracker.update_task(task_id, "processing", progress={"step": "saving_to_csv"})
        bundles_df = pd.DataFrame(bundles)
        leftovers_df = pd.DataFrame(leftovers)
        bundles_df.to_csv("bundles.csv", index=False)
        leftovers_df.to_csv("leftovers.csv", index=False)

        # save to json pandas
        task_tracker.update_task(task_id, "processing", progress={"step": "saving_to_json"})
        bundles_df.to_json("bundles.json", orient="records", lines=True)
        leftovers_df.to_json("leftovers.json", orient="records", lines=True)

        task_tracker.update_task(task_id, "completed", response_data)

    except Exception as e:
        error_msg = f"Pipeline processing failed: {str(e)}"
        logging.error(error_msg)
        task_tracker.update_task(task_id, "failed", {"error": error_msg})


@router.post("/search")
async def search_products(
    background_tasks: BackgroundTasks,
    query: str = Form(...),
    category: str = Form(None)
):
    """Start a background search task and return task ID."""
    task_id = task_tracker.create_task("search")
    background_tasks.add_task(process_search_task, task_id, query, category)
    return JSONResponse(
        content={"task_id": task_id, "status": "pending"},
        status_code=202
    )


@router.post("/translate")
async def translate_products(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Start a background translation task and return task ID."""
    task_id = task_tracker.create_task("translate")
    contents = await file.read()
    background_tasks.add_task(process_translate_task, task_id, contents)
    return JSONResponse(
        content={"task_id": task_id, "status": "pending"},
        status_code=202
    )


@router.post("/bundle")
async def create_bundles(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    lures_per_bundle: int = Form(...),
    min_usd_value: float = Form(...),
    target_yen_per_lure: float = Form(...),
):
    """Start a background bundle creation task and return task ID."""
    task_id = task_tracker.create_task("bundle")
    contents = await file.read()
    background_tasks.add_task(
        process_bundle_task,
        task_id,
        contents,
        lures_per_bundle,
        min_usd_value,
        target_yen_per_lure
    )
    return JSONResponse(
        content={"task_id": task_id, "status": "pending"},
        status_code=202
    )


@router.post("/convert")
async def convert_currency(
    background_tasks: BackgroundTasks,
    amount: float = Form(...),
    from_currency: str = Form(...),
    to_currency: str = Form(...),
):
    """Start a background currency conversion task and return task ID."""
    task_id = task_tracker.create_task("currency")
    background_tasks.add_task(
        process_currency_task,
        task_id,
        amount,
        from_currency,
        to_currency
    )
    return JSONResponse(
        content={"task_id": task_id, "status": "pending"},
        status_code=202
    )


async def stream_task_updates(task_id: str) -> AsyncGenerator[str, None]:
    """Stream task updates as they become available."""
    while True:
        task = task_tracker.get_task(task_id)
        if not task:
            yield "data: Task not found\n\n"
            break
            
        if task["status"] in ["completed", "failed"]:
            yield f"data: {jsonable_encoder(task)}\n\n"
            break
            
        yield f"data: {jsonable_encoder(task)}\n\n"
        await asyncio.sleep(0.5)


@router.get("/tasks/{task_id}/stream")
async def stream_task_status(task_id: str):
    """Stream task status updates using Server-Sent Events."""
    return StreamingResponse(
        stream_task_updates(task_id),
        media_type="text/event-stream"
    )


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a specific task."""
    task = task_tracker.get_task(task_id)
    if not task:
        return JSONResponse(
            content={"error": "Task not found"},
            status_code=404
        )
    
    if task["status"] == "processing":
        return JSONResponse(
            content={
                "status": task["status"],
                "result": task["result"],
                "progress": task.get("progress", {}),
                "task_id": task_id
            },
            status_code=200
        )
    
    return JSONResponse(content=task, status_code=200)


@router.get("/tasks")
async def list_tasks():
    """List all tasks."""
    tasks = task_tracker.list_tasks()
    return JSONResponse(content=tasks, status_code=200)


def clean_floats(obj, _processed=None):
    """Clean float values to be JSON compliant."""
    if _processed is None:
        _processed = set()
    
    # Handle circular references
    if id(obj) in _processed:
        return None
    _processed.add(id(obj))
    
    try:
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
            if abs(obj) > 1e10 or (abs(obj) < 1e-10 and obj != 0):
                return round(obj, 10)
            return obj
        elif isinstance(obj, dict):
            return {k: clean_floats(v, _processed) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_floats(i, _processed) for i in obj]
        elif hasattr(obj, "dict"):
            return clean_floats(obj.dict(), _processed)
        elif hasattr(obj, "__dict__"):
            return clean_floats(obj.__dict__, _processed)
        else:
            return obj
    except Exception as e:
        logging.error(f"Error cleaning floats: {str(e)}")
        return str(obj)  # Fallback to string representation


async def check_task_status(task_id: str):
    """Check the status of a task using a separate HTTP request."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f'/api/tasks/{task_id}')
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Progress: {data['progress']}")
