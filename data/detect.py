def is_korean_stock(ticker):
    # 숫자로만 되어 있으면 한국 종목 코드로 간주
    return ticker.isdigit()
