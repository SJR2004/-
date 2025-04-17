from pykrx import stock
import pandas as pd
from datetime import datetime

# 감성 분석 점수 더미 (실제 분석 붙이기 전 임시)
def get_sentiment_by_date(company_name, start, end):
    dates = pd.date_range(start, end)
    df = pd.DataFrame({"날짜": dates, "news_sentiment": [0.5] * len(dates)})
    return df

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_kr_stock_data(code, company_name="삼성전자", start="2023-01-01", end=None):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    # 가격 정보
    df_price = stock.get_market_ohlcv_by_date(start, end, code)
    df_price["MA20"] = df_price["종가"].rolling(window=20).mean()
    df_price["MA60"] = df_price["종가"].rolling(window=60).mean()
    df_price["Vol_Avg20"] = df_price["거래량"].rolling(window=20).mean()
    df_price["RSI"] = calculate_rsi(df_price["종가"])
    df_price = df_price.rename(columns={"종가": "close"})

    # 기본적 지표
    df_fundamental = stock.get_market_fundamental_by_date(start, end, code)

    # 뉴스 감성 점수
    df_sentiment = get_sentiment_by_date(company_name, start, end)

    # 통합
    df = pd.concat([df_price, df_fundamental], axis=1)

    # ROE/PBR/PER 누락될 수 있으므로 기본값 보정
    for col in ["PER", "PBR", "ROE"]:
        if col not in df.columns:
            df[col] = 0

    df = df.reset_index().merge(df_sentiment, left_on="날짜", right_on="날짜", how="left")
    df = df.dropna()

    return df[["날짜", "close", "MA20", "MA60", "Vol_Avg20", "RSI", "PER", "PBR", "ROE", "news_sentiment"]]
