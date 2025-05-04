import pandas as pd
import re


class DataProcessor(object):
    def __init__(self):
        pass

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """remove duplicates from dataframe"
        """
        print("length data before duplicates dataframe: ", len(df))
        removed = df.drop_duplicates()
        print("length data after duplicates dataframe: ", len(removed))
        return removed

    def extract_price(self, price_string: str) -> str:
        """Menghapus huruf dan simbol dari string harga dan mengembalikan nilai numerik."""
        return re.sub(r"[^0-9.]", "", price_string)
