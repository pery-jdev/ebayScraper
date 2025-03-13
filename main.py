from manager.product_translate import ProductTranslateManager
from services.processor.file_processor import FileProcessor

def main():
    file_processor = FileProcessor()
    product_manager = ProductTranslateManager()
    translated_products = product_manager.translate_product()
    file_processor.write_csv(translated_products, "translated_product.csv")



if __name__ == "__main__":
    main()