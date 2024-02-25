# -*- coding:UTF-8 -*-
import pandas as pd

from utils import BillRecord
from utils import strip_in_data, fuzzy_match_file_name
from .base_retriever import BaseRetriever

class AlipayRetriever(BaseRetriever):
    def __init__(self) -> None:
        super().__init__()
        self.source_str = "支付宝"
        self.fuzzy_file_name = "alipay"

    def read_csv_data(self, ctx, data_path):
        super().read_csv_data(ctx, data_path)
        df = pd.read_csv(data_path, header=0, skiprows=24, encoding='gbk')
        df = strip_in_data(df)  # 去除列名与数值中的空格。
        df['交易订单号'] = df['交易订单号'].str.strip('\t')
        return df

    def filter_refund(self, ctx):
        refunds = self.raw_data[self.raw_data["交易状态"] == "退款成功"]
        filter_original_cnt = 0
        for refund_order in refunds.itertuples():
            original_order_id = getattr(refund_order, '交易订单号').split('_')[0]
            original_order = self.raw_data[self.raw_data["交易订单号"] == original_order_id]
            original_amount = getattr(original_order, "金额").iloc[0]
            refund_amount = getattr(refund_order, '金额')
            if original_amount == refund_amount:
                filter_original_cnt += 1
                self.raw_data = self.raw_data.drop(original_order.index)
            else:
                self.raw_data.loc[original_order.index, "金额"] = original_amount - refund_amount
                self.raw_data.loc[original_order.index, "商品说明"] += "(with退款)"
        self.raw_data = self.raw_data.drop(refunds.index)
        ctx.info_log.write("filter_refund", refunds.shape[0])
        ctx.info_log.write("filter_refund_original", filter_original_cnt)

    def filter(self, ctx):
        self.filter_refund(ctx)
        super().filter(ctx)

