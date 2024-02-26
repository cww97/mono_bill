# -*- coding:UTF-8 -*-
import pandas as pd

from .base_retriever import BaseRetriever, strip_in_data

class BankICBCRetriever(BaseRetriever):
    def __init__(self) -> None:
        super().__init__()
        self.source_str = "工商银行"
        self.fuzzy_file_name = "hisdetail"

    def read_csv_data(self, ctx, data_path):
        super().read_csv_data(ctx, data_path)
        df = pd.read_csv(data_path, header=0, skiprows=6, encoding='utf-8', index_col=False)
        df = strip_in_data(df.drop(index=[df.shape[0]-1]))
        df.rename(columns={'交易日期': '交易时间', '对方户名': '交易对方', "摘要": "交易分类", "交易场所": "商品说明"}, inplace=True)
        return df

    def fine_tune(self, ctx):
        self.raw_data["交易金额(收入)"] = self.raw_data["交易金额(收入)"].replace('', '0').str.replace(',', '').astype(float)
        self.raw_data["交易金额(支出)"] = 0 - self.raw_data["交易金额(支出)"].replace('', '0').str.replace(',', '').astype(float)
        self.raw_data["金额"] = self.raw_data["交易金额(收入)"] + self.raw_data["交易金额(支出)"]
        self.raw_data["收支"] = "收入"
        super().fine_tune(ctx)
        # self.raw_data.to_csv('data/tmp/tmp.csv')

    def filter(self, ctx):
        self.raw_data = self.raw_data.drop(self.raw_data[self.raw_data["商品说明"].str.contains("支付宝")].index)
        self.raw_data = self.raw_data.drop(self.raw_data[self.raw_data["商品说明"].str.contains("财付通")].index)
        self.raw_data = self.raw_data.drop(self.raw_data[self.raw_data["交易对方"].str.contains("陈伟文")].index)
        if self.raw_data[self.raw_data["交易币种"]!="人民币"].shape[0] > 0:
            raise Exception(f"存在非人民币交易，请手动处理")
        ctx.info_log.write("after_filter", self.raw_data.shape[0])
