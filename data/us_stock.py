import yfinance as yf
import pandas as pd
from datetime import datetime

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_us_stock_data(ticker):
    end = datetime.today().strftime("%Y-%m-%d")
    start = "2023-01-01"

    data = yf.download(ticker, start=start, end=end)
    df = data.copy()

    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA60"] = df["Close"].rolling(window=60).mean()
    df["Vol_Avg20"] = df["Volume"].rolling(window=20).mean()
    df["RSI"] = calculate_rsi(df["Close"])
    df["news_sentiment"] = 0.5  # 더미 값

    df = df.dropna()
    df = df.rename(columns={"Close": "close"})

    return df[["close", "MA20", "MA60", "Vol_Avg20", "RSI", "news_sentiment"]]
