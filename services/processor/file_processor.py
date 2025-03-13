import pandas as pd
from core.config import config as cfg


class FileProcessor:
    def __init__(self):
        pass

    def read_csv(self, path: str):
        """read CSV from data directory

        Args:
            path (str): filename from data directory
        """
        return pd.read_csv(f"{cfg.DATA_DIR}/{path}")

    def write_csv(self, df: pd.DataFrame, path: str):
        """write CSV to data directory

        Args:
            df (pd.DataFrame): dataframe to write
            path (str): filename from data directory
        """
        return df.to_csv(f"{cfg.DATA_DIR}/{path}", index=False)
