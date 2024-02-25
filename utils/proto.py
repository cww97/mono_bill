# -*- coding:UTF-8 -*-
from datetime import datetime
from dataclasses import dataclass

@dataclass
class BillRecord:
    date: datetime          # 日期时间
    oppo_account: str       # 交易对方
    description: str        # 商品说明
    amount: float           # 金额
    queue: str              # 队列: daily/huge
    category: str           # 分类: based on 支付宝
    source: str             # 来源: 支付宝/微信/抖音/银行/其他
    # extra: dict[str, str]   # 备注

@dataclass
class RequestContext:
    bill_records: list[BillRecord]

    def __init__(self) -> None:
        self.year = datetime.now().year
        self.bill_records = []

        self.info_log = MonoLogger("INFO")
        # self.debug_log = MonoLogger()
        # self.warn_log = MonoLogger()
        # self.error_log = MonoLogger()

class MonoLogger:
    def __init__(self, level) -> None:
        self.level = level
        self.raw_log = ""

    def write(self, msg):
        self.raw_log += f"{msg} "

    def write(self, key, value):
        self.raw_log += f"{key}={value} "

    def flush(self, module_name):
        output = f"{datetime.now()} {self.level} [{module_name}] {self.raw_log.strip()}"
        print(output)
        self.raw_log = ""