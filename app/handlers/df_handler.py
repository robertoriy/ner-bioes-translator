import pandas as pd
from typing import Optional

class DataFrameHandler:
    def __init__(self):
        self._df: Optional[pd.DataFrame] = None

    def set_dataframe(self, df: pd.DataFrame) -> None:
        """Сохраняет DataFrame в менеджере"""
        self._df = df.copy()

    def get_dataframe(self) -> pd.DataFrame:
        """Возвращает сохраненный DataFrame"""
        if self._df is None:
            raise ValueError("DataFrame не загружен")
        return self._df

df_handler = DataFrameHandler()
result_df_handler = DataFrameHandler()