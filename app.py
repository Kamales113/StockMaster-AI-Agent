from fastapi import FastAPI
import yfinance as yf
from ta.momentum import RSIIndicator

app = FastAPI()

@app.get("/analyze")
def analyze_stock(symbol: str):

    stock = yf.download(symbol, period="3mo")

    if stock.empty:
        return {"error": "Invalid stock symbol"}

    close_prices = stock['Close'].squeeze()

    rsi = RSIIndicator(close_prices).rsi().iloc[-1]

    current_price = close_prices.iloc[-1]

    if rsi > 70:
        signal = "Overbought"
    elif rsi < 30:
        signal = "Oversold"
    else:
        signal = "Neutral"

    return {
        "stock": symbol,
        "price": round(float(current_price), 2),
        "RSI": round(float(rsi), 2),
        "signal": signal
    }