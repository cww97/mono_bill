# -*- coding:UTF-8 -*-
import pandas as pd

from utils import BillRecord
from utils import strip_in_data, fuzzy_match_file_name
from .base_retriever import BaseRetriever

class WechatRetriever(BaseRetriever):
    def __init__(self) -> None:
        super().__init__()
        self.source_str = "微信"
        self.fuzzy_file_name = "微信"

    def read_csv_data(self, ctx, data_path):
        super().read_csv_data(ctx, data_path)
        df = pd.read_csv(data_path, header=0, skiprows=16, encoding='utf-8')
        df = strip_in_data(df)  # 去除列名与数值中的空格
        df.rename(columns={'金额(元)': '金额', '商品': '商品说明', "交易类型": "交易分类"}, inplace=True)
        return df

    def fine_tune(self, ctx):
        self.raw_data["金额"] = self.raw_data["金额"].str.strip('¥').astype('float')
        super().fine_tune(ctx)
        # self.raw_data.to_csv('data/tmp.csv')