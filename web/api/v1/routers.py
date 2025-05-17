import pandas as pd
import logging
import io

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
        # The translate_product method likely takes a DataFrame and returns a translated DataFrame
        df = translate_manager.translate_product(df)

        # 3. Search for Product Prices (USD & AUD)
        # Call the new method in product_manager to add pricing
        df = product_manager.add_pricing_to_dataframe(df)

        # 4. Perform Currency Conversion (if needed for bundling rules)
        # This step is now handled within add_pricing_to_dataframe where AUD is converted to USD.
        # Ensure that the 'Cost in Yen' column exists and is appropriately named for bundle creation.
        # If necessary, ensure data types for price_usd, price_aud, and cost in yen are numeric.

        # 5. Create Bundles Based on Specific Rules and Identify Leftovers
        # This step uses the logic from the /bundle endpoint
        # Ensure product_manager.generate_bundles uses the 'price_usd', 'price_aud', and 'Cost in Yen' columns
        bundles = product_manager.generate_bundles(
            df, # Pass the DataFrame with translated names and prices
            lures_per_bundle,
            min_usd_value,
            target_yen_per_lure
        )

        # 6. Return Results
        # The bundles object should contain both the bundles and leftover information
        return JSONResponse(content=bundles, status_code=200)

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        return JSONResponse(
            content={"error": f"Pipeline processing failed: {str(e)}"},
            status_code=500
        )

# buatkan endpoint untuk process tahap 1
