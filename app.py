from flask import Flask, render_template, request
from data.kr_stock import get_kr_stock_data
from data.us_stock import get_us_stock_data
from data.detect import is_korean_stock
from models.predict import predict_stock
from data.code_map import get_code_by_name # 회사명 -> 종목코드 변환

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        ticker = request.form["ticker"].strip()

        # 👇 회사명을 입력한 경우 → 종목코드로 변환 시도
        if not ticker.isdigit():
            converted = get_code_by_name(ticker)
            if converted:
                ticker = converted
            else:
                result = {"error": "❌ 회사명을 찾을 수 없습니다."}
                return render_template("index.html", result=result)

        try:
            if is_korean_stock(ticker):
                df = get_kr_stock_data(ticker, company_name=ticker)  # ticker를 회사명으로 전달
            else:
                df = get_us_stock_data(ticker)

            result = predict_stock(df)

        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

