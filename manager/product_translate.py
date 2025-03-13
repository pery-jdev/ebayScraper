import logging
import pandas as pd

from typing import List, Optional
from services.processor.file_processor import FileProcessor
from services.translations.translator import MultiTranslator


class ProductTranslateManager:
    def __init__(self):
        self.file_processor: FileProcessor = FileProcessor()
        self.translator: MultiTranslator = MultiTranslator()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def translate_product(self, columns: Optional[List[str]] = None):
        try:
            products = self.file_processor.read_csv("product.csv")

            if products is None:
                self.logger.error("Failed to read input file")
                return None
            
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
                        
                        # Proses translasi
                        translated = self.translator.translate_text(text=text_to_translate,)
                        
                        # Kembalikan ke tipe data asli
            
                        
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
