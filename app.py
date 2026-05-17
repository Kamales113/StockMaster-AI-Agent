from fastapi import FastAPI
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD
import talib

app = FastAPI()


@app.get("/")
def home():
    return {"message": "StockMaster API Running"}


@app.get("/analyze")
def analyze_stock(symbol: str):

    stock = yf.download(symbol, period="6mo")

    if stock.empty:
        return {"error": "Invalid stock symbol"}

    close_prices = stock['Close'].squeeze()
    # Candlestick Pattern Detection

    # Candlestick Pattern Detection

    open_price = stock['Open'].values.flatten()
    high_price = stock['High'].values.flatten()
    low_price = stock['Low'].values.flatten()
    close_price = stock['Close'].values.flatten()

    patterns = {}

    # Doji
    patterns["Doji"] = talib.CDLDOJI(
        open_price,
        high_price,
        low_price,
        close_price
    )[-1]

    # Hammer
    patterns["Hammer"] = talib.CDLHAMMER(
        open_price,
        high_price,
        low_price,
        close_price
    )[-1]

    # Engulfing
    patterns["Engulfing"] = talib.CDLENGULFING(
        open_price,
        high_price,
        low_price,
        close_price
    )[-1]

    # Morning Star
    patterns["Morning Star"] = talib.CDLMORNINGSTAR(
        open_price,
        high_price,
        low_price,
        close_price
    )[-1]

    # Shooting Star
    patterns["Shooting Star"] = talib.CDLSHOOTINGSTAR(
        open_price,
        high_price,
        low_price,
        close_price
    )[-1]

    # Harami
    patterns["Harami"] = talib.CDLHARAMI(
        open_price,
        high_price,
        low_price,
        close_price
    )[-1]


    detected_patterns = []

    for pattern_name, value in patterns.items():

        if value > 0:
            detected_patterns.append(f"Bullish {pattern_name}")

        elif value < 0:
            detected_patterns.append(f"Bearish {pattern_name}")

    if len(detected_patterns) == 0:
        candlestick_pattern = "No Major Pattern"

    else:
        candlestick_pattern = ", ".join(detected_patterns)

    # RSI
    rsi = RSIIndicator(close_prices).rsi().iloc[-1]

    # Moving Averages
    ma20 = close_prices.rolling(window=20).mean().iloc[-1]
    ma50 = close_prices.rolling(window=50).mean().iloc[-1]

    # MACD
    macd = MACD(close_prices)

    macd_value = macd.macd().iloc[-1]
    signal_value = macd.macd_signal().iloc[-1]

    current_price = close_prices.iloc[-1]

    # RSI Signal
    if rsi > 70:
        rsi_signal = "Overbought"
    elif rsi < 30:
        rsi_signal = "Oversold"
    else:
        rsi_signal = "Neutral"

    # Trend Signal
    if ma20 > ma50:
        trend = "Bullish Trend"
    else:
        trend = "Bearish Trend"

    # MACD Signal
    if macd_value > signal_value:
        macd_signal = "Bullish Momentum"
    else:
        macd_signal = "Bearish Momentum"

    # Confidence Score
    confidence_score = 0

    # RSI Weight
    if rsi < 70:
        confidence_score += 30

    # Trend Weight
    if ma20 > ma50:
        confidence_score += 35

    # MACD Weight
    if macd_value > signal_value:
        confidence_score += 35

    # Final Recommendation
    if confidence_score >= 70:
        recommendation = "BUY"
    elif confidence_score >= 40:
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    return {
        "stock": symbol,
        "price": round(float(current_price), 2),
        "RSI": round(float(rsi), 2),
        "RSI Signal": rsi_signal,
        "Trend": trend,
        "MACD Signal": macd_signal,
        "Candlestick Pattern": candlestick_pattern,
        "Recommendation": recommendation,
        "Confidence": f"{confidence_score}%"
    }


@app.get("/compare")
def compare_stocks(symbol1: str, symbol2: str):

    def get_stock_score(symbol):

        stock = yf.download(symbol, period="6mo")

        if stock.empty:
            return None

        close_prices = stock['Close'].squeeze()

        # RSI
        rsi = RSIIndicator(close_prices).rsi().iloc[-1]

        # Moving Averages
        ma20 = close_prices.rolling(window=20).mean().iloc[-1]
        ma50 = close_prices.rolling(window=50).mean().iloc[-1]

        # MACD
        macd = MACD(close_prices)

        macd_value = macd.macd().iloc[-1]
        signal_value = macd.macd_signal().iloc[-1]

        confidence_score = 0

        # RSI Weight
        if rsi < 70:
            confidence_score += 30

        # Trend Weight
        if ma20 > ma50:
            confidence_score += 35

        # MACD Weight
        if macd_value > signal_value:
            confidence_score += 35

        return {
            "symbol": symbol,
            "score": confidence_score,
            "RSI": round(float(rsi), 2),
            "Trend": "Bullish" if ma20 > ma50 else "Bearish",
            "Momentum": "Bullish" if macd_value > signal_value else "Bearish"
        }

    stock1 = get_stock_score(symbol1)
    stock2 = get_stock_score(symbol2)

    if stock1 is None or stock2 is None:
        return {"error": "Invalid stock symbol"}

    if stock1["score"] > stock2["score"]:
        better_stock = stock1["symbol"]
    elif stock2["score"] > stock1["score"]:
        better_stock = stock2["symbol"]
    else:
        better_stock = "Both stocks are equally strong"

    return {
        "Stock 1": stock1,
        "Stock 2": stock2,
        "Better Stock": better_stock
    }