import pandas as pd
import logging
import io
import math

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

from dto.requests.product_request_sdc import ProductDetailsRequestSDC as ProductDetailRequest
from manager.product_manager import EbayProductManager
from manager.product_translate import ProductTranslateManager
from manager.currency_manager import CurrencyManager
from services.processors.file_processor import FileProcessor
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix="/api")
product_manager = EbayProductManager()
translate_manager = ProductTranslateManager()
currency_manager = CurrencyManager()
file_processor = FileProcessor()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/search")
async def search_products(query: str = Form(...), category: str = Form(None)):
    try:
        products = product_manager.get_products(query=query, category=category)
        return JSONResponse(content=products, status_code=200)
    except Exception as e:
        logging.error(f"Search failed: {str(e)}")
        return JSONResponse(
            content={"error": "Product search failed"},
            status_code=500
        )

@router.post("/translate")
async def translate_products(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        translated = translate_manager.translate_product(df)
        return JSONResponse(content=translated.to_dict('records'), status_code=200)
    except Exception as e:
        logging.error(f"Translation failed: {str(e)}")
        return JSONResponse(
            content={"error": "Product translation failed"},
            status_code=500
        )

@router.post("/bundle")
async def create_bundles(
    file: UploadFile = File(...),
    lures_per_bundle: int = Form(...),
    min_usd_value: float = Form(...),
    target_yen_per_lure: float = Form(...)
):
    try:
        contents = await file.read()
        df = pd.read_csv(contents)
        bundles = product_manager.generate_bundles(
            df,
            lures_per_bundle,
            min_usd_value,
            target_yen_per_lure
        )
        return JSONResponse(content=bundles, status_code=200)
    except Exception as e:
        logging.error(f"Bundle creation failed: {str(e)}")
        return JSONResponse(
            content={"error": "Bundle creation failed"},
            status_code=500
        )

@router.post("/convert")
async def convert_currency(
    amount: float = Form(...),
    from_currency: str = Form(...),
    to_currency: str = Form(...)
):
    try:
        converted = currency_manager.calculate_price_map(from_currency, amount)
        return JSONResponse(
            content={"convertedAmount": converted.get(to_currency)},
            status_code=200
        )
    except Exception as e:
        logging.error(f"Currency conversion failed: {str(e)}")
        return JSONResponse(
            content={"error": "Currency conversion failed"},
            status_code=500
        )
    

@router.post("/process")
async def process_file(file: UploadFile = File(...)):

    # read file
    contents = await file.read()
    df = pd.read_csv(contents)
    return JSONResponse(content=df.to_dict('records'), status_code=200)

@router.get("/detail")
def test_detail():
    data = product_manager.test_product_detail()
    data = jsonable_encoder(data)
    
    return JSONResponse(content=data, status_code=200)

@router.post("/pipeline")
async def run_pipeline(
    file: UploadFile = File(...),
    lures_per_bundle: int = Form(...),
    min_usd_value: float = Form(...),
    target_yen_per_lure: float = Form(...)
):
    try:
        # 1. Read the CSV file
        df = pd.read_csv(file.file)

        # 2. Translate Product Names
        df = translate_manager.translate_product(df)

        # 3. Search for Product Prices (USD & AUD)
        df = product_manager.add_pricing_to_dataframe(df)

        # 4. Create Bundles Based on Specific Rules and Identify Leftovers
        bundles, leftovers = product_manager.generate_bundles(
            df,
            lures_per_bundle,
            min_usd_value,
            target_yen_per_lure
        )

        # Clean and prepare the response
        cleaned_bundles = clean_floats(bundles)
        cleaned_leftovers = clean_floats(leftovers)
        
        response_data = {
            "bundles": cleaned_bundles,
            "leftovers": cleaned_leftovers
        }

        # Save as json and csv with pandas for response_data
        # Save bundles and leftovers as JSON
        bundles_df = pd.DataFrame(cleaned_bundles)
        leftovers_df = pd.DataFrame(cleaned_leftovers)

        bundles_df.to_json("bundles.json", orient="records", force_ascii=False)
        leftovers_df.to_json("leftovers.json", orient="records", force_ascii=False)

        # Save bundles and leftovers as CSV
        bundles_df.to_csv("bundles.csv", index=False)
        leftovers_df.to_csv("leftovers.csv", index=False)
        
        return JSONResponse(content=jsonable_encoder(response_data), status_code=200)

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        return JSONResponse(
            content={"error": f"Pipeline processing failed: {str(e)}"},
            status_code=500
        )

def clean_floats(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: clean_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_floats(i) for i in obj]
    elif hasattr(obj, 'dict'):  # Handle Pydantic models
        return clean_floats(obj.dict())
    elif hasattr(obj, '__dict__'):  # Handle other objects with __dict__
        return clean_floats(obj.__dict__)
    else:
        return obj
