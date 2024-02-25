# -*- coding:UTF-8 -*-
import pandas as pd

from utils import strip_in_data
from .base_retriever import BaseRetriever

class HandwriteRetriever(BaseRetriever):
    def __init__(self) -> None:
        super().__init__()
        self.source_str = "手动录入"
        self.fuzzy_file_name = "手动录入"

    def read_csv_data(self, ctx, data_path):
        super().read_csv_data(ctx, data_path)
        df = pd.read_csv(data_path, header=0, encoding='gbk', index_col=False)
        df = strip_in_data(df).dropna(how="all")
        df["交易对方"] = ""
        # import ipdb; ipdb.set_trace()
        return df