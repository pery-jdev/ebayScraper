from services.bundles.bundle_engine import BundleEngine
from manager.currency_manager import CurrencyManager
from manager.product_translate import ProductTranslateManager
from services.processors.file_processor import FileProcessor
import logging

def main_workflow(input_file="product.csv", output_file="bundles_report.csv"):
    """Main workflow to process products from CSV to bundles"""
    try:
        # Initialize components
        file_processor = FileProcessor()
        translator = ProductTranslateManager()
        currency_manager = CurrencyManager()

        # 1. Read input CSV
        logging.info("Reading input file...")
        products = file_processor.read_csv(input_file)
        
        # 2. Translate products
        logging.info("Translating products...")
        translated_products = translator.translate_product(products)
        
        # 3. Calculate pricing
        logging.info("Calculating prices...")
        for index, product in translated_products.iterrows():
            try:
                base_currency = product['cost_currency']
                base_amount = product['cost']
                price_map = currency_manager.calculate_price_map(base_currency, base_amount)
                translated_products.at[index, 'price_map'] = price_map
            except Exception as e:
                logging.warning(f"Failed to calculate prices for product {index}: {str(e)}")
                translated_products.at[index, 'price_map'] = {}
        
        # 4. Generate bundles
        logging.info("Generating bundles...")
        bundle_engine = BundleEngine(translated_products.to_dict('records'))
        bundles, leftovers = bundle_engine.generate_bundles()
        
        # 5. Write output
        logging.info("Writing output...")
        file_processor.write_csv(bundles, output_file)
        
        logging.info("Workflow completed successfully")
        return True
        
    except Exception as e:
        logging.error(f"Workflow failed: {str(e)}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main_workflow()
