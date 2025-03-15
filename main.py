from manager.product_translate import ProductTranslateManager
from manager.product_manager import ProductManager
# from services.processors.file_processor import FileProcessor

def main():
    # file_processor = FileProcessor()
    # product_manager = ProductTranslateManager()
    # translated_products = product_manager.translate_product()
    # file_processor.write_csv(translated_products, "translated_product.csv")
    product_manager = ProductManager()
    product_manager.get_products()



if __name__ == "__main__":
    main()