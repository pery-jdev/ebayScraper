import logging
import pandas as pd

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

    def translate_product(
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
                
                # iterate using iterrows instead of range
                for index, row in translated_products.iterrows():
                    log_file.write(f"\n--- Row {index} ---\n")
                    
                    for col in valid_columns:
                        original_value = row[col]

                        # Skip nilai kosong atau non-string
                        if pd.isna(original_value) or not isinstance(original_value, str):
                            continue

                        try:
                            # Convert to string untuk translasi
                            text_to_translate = str(original_value).strip()
                            
                            # Skip empty strings
                            if not text_to_translate:
                                continue

                            # Cek cache dulu
                            if text_to_translate in self.translation_cache:
                                translated = self.translation_cache[text_to_translate]
                                self.logger.debug(
                                    f"Using cached translation for: {text_to_translate}"
                                )
                            else:
                                self.logger.debug(f"Translating: {text_to_translate}")
                                try:
                                    translated = self.translator.translate_text(
                                        text=text_to_translate
                                    )
                                    if translated:
                                        self.translation_cache[text_to_translate] = translated
                                        self.logger.debug(f"New translation: {translated}")
                                    else:
                                        self.logger.warning(
                                            f"Empty translation result for: {text_to_translate}"
                                        )
                                        translated = original_value
                                except Exception as trans_e:
                                    self.logger.error(
                                        f"Translation error for text '{text_to_translate}': {str(trans_e)}"
                                    )
                                    translated = original_value

                            # Log translation details
                            log_file.write(
                                f"Column: {col}\n"
                                f"Original: {text_to_translate}\n"
                                f"Translated: {translated}\n"
                                f"{'='*50}\n"
                            )

                            # Update the value in the DataFrame
                            translated_products.at[index, col] = translated

                        except Exception as e:
                            self.logger.error(
                                f"Translation failed for column '{col}' at index {index}: {str(e)}\n"
                                f"Original text: '{text_to_translate}'"
                            )
                            translated_products.at[index, col] = original_value
                            
                            # Log error in translation details
                            log_file.write(
                                f"Column: {col}\n"
                                f"Original: {text_to_translate}\n"
                                f"Error: {str(e)}\n"
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
