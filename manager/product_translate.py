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
        self.translator: MultiTranslator = MultiTranslator(translator='translators')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.translation_cache = {}

    def translate_product(self, products: pd.DataFrame, columns: Optional[List[str]] = None):
        try:
            if products is None or products.empty:
                self.logger.error("Invalid input products DataFrame")
                return None
                
            products = self.data_processor.remove_duplicates(products)
            
            # create new dataframe to Accommodate new products
            translated_products = products.copy()

            # translate all columns 
            if not columns:
                columns = translated_products.columns.tolist()
        

            valid_columns =  [col for col in columns if col in products.columns]

            # iterate valid column
            # Iterasi semua baris dan kolom
            for index in range(len(translated_products)):
                for col in valid_columns:
                    original_value = translated_products.at[index, col]
                    
                    # Skip nilai kosong
                    if pd.isna(original_value):
                        continue
                    
                    try:
                        # Convert to string untuk translasi
                        text_to_translate = str(original_value)
                        
                        # Cek cache dulu
                        if text_to_translate in self.translation_cache:
                            translated = self.translation_cache[text_to_translate]
                        else:
                            translated = self.translator.translate_text(text=text_to_translate)
                            self.translation_cache[text_to_translate] = translated  # Simpan ke cache
                        
                        translated_products.at[index, col] = translated
                        
                        # Debug output
                        print(f"Translated [{index},{col}]: {original_value} -> {translated}")
                        
                    except Exception as e:
                        self.logger.warning(f"Gagal translate {col} index {index}: {str(e)}")
                        translated_products.at[index, col] = original_value  # Kembalikan nilai asli
            
            
            return translated_products
            
        except Exception as e:
            self.logger.error(f"Error utama: {str(e)}")
            return None

        except Exception as e:
            self.logger.error(f"Error during translation: {e}")
