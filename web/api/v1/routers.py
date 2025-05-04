import pandas as pd
import logging

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

from manager.product_manager import EbayProductManager
from manager.product_translate import ProductTranslateManager
from manager.currency_manager import CurrencyManager
from services.processors.file_processor import FileProcessor


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
        df = pd.read_csv(contents)
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
    return JSONResponse(content=data, status_code=200)