# -*- coding:UTF-8 -*-
from utils import BillRecord, fuzzy_match_file_name

def strip_in_data(df):
    df = df.rename(columns={column_name: column_name.strip().replace('/', '') for column_name in df.columns})
    df = df.apply(lambda x: x.str.strip().replace('\t', '') if x.dtype == "object" else x)
    return df

class BaseRetriever:
    def __init__(self) -> None:
        self.skip_retriever = False
        self.raw_data = None

    def fetch(self, ctx):
        self.req_data(ctx)
        if not self.skip_retriever:
            self.fine_tune(ctx)
            self.filter(ctx)
            self.pack(ctx)

        ctx.info_log.flush(self.__class__.__name__)
   
    def read_csv_data(self, ctx, data_path):
        ctx.info_log.write("csv", data_path)
    def req_data(self, ctx):
        data_path = fuzzy_match_file_name(self.fuzzy_file_name)
        if data_path == "":
            self.skip_retriever = True
            ctx.info_log.write("skip_retriever", 1)
        else:
            self.raw_data = self.read_csv_data(ctx, data_path)
            ctx.info_log.write("req_data", self.raw_data.shape[0])

    def check_self_trans_white_list(self, description):
        white_list = ("收益发放", "自动转入", "转账收款到余额宝", "转入零钱通")
        for word in white_list:
            if word in description:
                return True
        return False
        raise Exception(f"self_trans order {description} not in white_list")
    def filter_self_trans(self, ctx):
        self_trans_orders = self.raw_data[(self.raw_data["收支"]!="收入")&(self.raw_data["收支"]!="支出")]
        for order in self_trans_orders.itertuples():
            description = f"{order.商品说明}:{order.交易对方}:{order.交易分类}"
            if not self.check_self_trans_white_list(description):
                print(order)
                raise Exception(f"self_trans order {description} not in white_list")
            # self.check_self_trans_white_list(description)
        self.raw_data = self.raw_data.drop(self_trans_orders.index)
        ctx.info_log.write("filter_self_trans", self_trans_orders.shape[0])
    def filter(self, ctx):
        self.filter_self_trans(ctx)
        ctx.info_log.write("after_filter", self.raw_data.shape[0])

    def fine_tune(self, ctx):
        self.raw_data['交易时间'] = self.raw_data['交易时间'].astype('datetime64[ns]')

    def decide_queue(self, record):
        if record.交易对方 in ("上海市宝山区大场医院", "上海市第十人民医院"):
            return "huge"
        if record.商品说明 in ["太平洋保险", "工资"]:
            return "huge"
        if "NUX" in record.商品说明:  # music
            return "huge"
        if "生活费用" in record.商品说明:
            return "daily"
        return "daily" if record.金额 < 500.00 else "huge"
    def pack(self, ctx):
        for record in self.raw_data.itertuples():
            ctx.bill_records.append(
                BillRecord(
                    date=record.交易时间,
                    oppo_account=record.交易对方,
                    description=record.商品说明,
                    amount=record.金额 if getattr(record, "收支") == "收入" else -record.金额,
                    queue=self.decide_queue(record),
                    category=record.交易分类,
                    source=self.source_str,
                    # extra={},
                )
            )
        ctx.info_log.write("pack", self.raw_data.shape[0])