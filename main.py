# -*- coding:UTF-8 -*-
from utils import RequestContext, fuzzy_match_file_name
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
    CwwSinker(ctx).fetch(ctx)

def main():
    conf_file = fuzzy_match_file_name("_conf.json")
    ctx = RequestContext(conf_file)

    recall(ctx)
    sort(ctx)
    sink(ctx)

if __name__ == "__main__":
    main()