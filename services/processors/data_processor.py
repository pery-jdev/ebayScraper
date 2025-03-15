import pandas as pd

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
