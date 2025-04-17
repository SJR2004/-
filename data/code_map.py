# data/code_map.py
from pykrx import stock

def get_code_by_name(name):
    df = stock.get_market_ticker_list(market="ALL")
    code_name_map = {stock.get_market_ticker_name(code): code for code in df}
    return code_name_map.get(name)
