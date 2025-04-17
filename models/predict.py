from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

def draw_prediction_chart(y_real, y_pred):
    plt.figure(figsize=(10, 5))
    plt.plot(y_real.index, y_real.values, label='📍 실제 종가', color='blue')
    plt.plot(y_real.index, y_pred, label='🔮 예측 종가', color='orange')
    plt.legend()
    plt.title("주가 예측 결과")
    plt.xlabel("날짜")
    plt.ylabel("가격")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/chart.png")
    plt.close()

def predict_stock(df):
    df = df.copy()
    df["target_price"] = df["close"].shift(-20)
    df = df.dropna()

    features = [col for col in df.columns if col not in ["날짜", "target_price"]]
    X = df[features]
    y = df["target_price"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    draw_prediction_chart(y_test, y_pred)

    latest = X_test.iloc[-1]
    current = y_test.values[-1]
    predicted = y_pred[-1]
    pct = (predicted - current) / current * 100

    if pct >= 2:
        recommendation = "Buy ✅"
    elif pct <= -2:
        recommendation = "Sell ❌"
    else:
        recommendation = "Hold 🟡"

    # 예측 결과 CSV 저장
    result_df = X_test.copy()
    result_df["actual"] = y_test.values
    result_df["predicted"] = y_pred
    result_df.to_csv("static/prediction_result.csv", index=False)

    return {
        "current_price": round(current, 2),
        "predicted_price": round(predicted, 2),
        "pct": round(pct, 2),
        "recommendation": recommendation
    }
