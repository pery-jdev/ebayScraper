import logging
import pandas as pd
import asyncio
from typing import List, Optional
from services.processors.file_processor import FileProcessor
from services.processors.data_processor import DataProcessor
from services.translations.translator import MultiTranslator


class ProductTranslateManager:
    def __init__(self):
        self.file_processor: FileProcessor = FileProcessor()
        self.data_processor: DataProcessor = DataProcessor()
        self.translator: MultiTranslator = MultiTranslator(translator="translators")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Add file handler
        fh = logging.FileHandler("translation.log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.translation_cache = {}

    async def translate_product(
        self, products: pd.DataFrame, columns: Optional[List[str]] = None
    ):
        try:
            if products is None or products.empty:
                self.logger.error("Invalid input products DataFrame")
                return None

            self.logger.info(f"Starting translation for {len(products)} products")
            products = self.data_processor.remove_duplicates(products)
            self.logger.info(f"After removing duplicates: {len(products)} products")

            # create new dataframe to Accommodate new products
            translated_products = products.copy()

            # translate all columns
            if not columns:
                # Only translate string columns
                columns = [
                    col for col in translated_products.columns 
                    if translated_products[col].dtype == 'object'
                ]

            valid_columns = [col for col in columns if col in products.columns]
            self.logger.info(f"Columns to translate: {valid_columns}")

            # Create translation log file
            with open("translation_details.log", "w", encoding="utf-8") as log_file:
                log_file.write("=== Translation Details ===\n\n")
                
                # Process translations in batches
                batch_size = 50
                for col in valid_columns:
                    # Get all non-null values for this column
                    texts_to_translate = []
                    indices = []
                    for index, value in translated_products[col].items():
                        if pd.notna(value) and isinstance(value, str) and value.strip():
                            texts_to_translate.append(value.strip())
                            indices.append(index)
                    
                    if not texts_to_translate:
                        continue

                    # Translate in batches
                    for i in range(0, len(texts_to_translate), batch_size):
                        batch = texts_to_translate[i:i + batch_size]
                        batch_indices = indices[i:i + batch_size]
                        
                        # Translate batch
                        translated_batch = await self.translator.translate_batch(batch)
                        
                        # Update DataFrame with translations
                        for batch_idx, (idx, translated) in enumerate(zip(batch_indices, translated_batch)):
                            if translated:
                                translated_products.at[idx, col] = translated
                                # Log translation
                                log_file.write(
                                    f"Column: {col}\n"
                                    f"Original: {batch[batch_idx]}\n"
                                    f"Translated: {translated}\n"
                                    f"{'='*50}\n"
                                )

            self.logger.info(
                f"Translation completed. Processed {len(translated_products)} products"
            )
            self.logger.info("Translation details saved to translation_details.log")
            return translated_products

        except Exception as e:
            self.logger.error(
                f"Critical error during translation: {str(e)}", exc_info=True
            )
            raise Exception(f"Translation failed: {str(e)}")
