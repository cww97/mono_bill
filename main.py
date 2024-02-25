# -*- coding:UTF-8 -*-
from utils import RequestContext
from module.data_provider import AlipayRetriever, WechatRetriever
from module.data_provider import BankICBCRetriever, HandwriteRetriever
from module.sinker.cww_sinker import CwwSinker

def recall(ctx):
    AlipayRetriever().fetch(ctx)
    WechatRetriever().fetch(ctx)
    BankICBCRetriever().fetch(ctx)
    HandwriteRetriever().fetch(ctx)

def sort(ctx):
    ctx.bill_records.sort(key=lambda x: x.date)
    ctx.year = ctx.bill_records[0].date.year

def sink(ctx):
    CwwSinker().fetch(ctx)

def main():
    ctx = RequestContext()
    recall(ctx)
    sort(ctx)
    sink(ctx)

if __name__ == "__main__":
    main()