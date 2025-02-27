import requests
import numpy as np
import time
from sklearn.linear_model import LinearRegression

# Binance API endpoints
BASE_URL = "https://api.binance.com/api/v3"
TICKER_URL = f"{BASE_URL}/ticker/24hr"
KLINE_URL = f"{BASE_URL}/klines"

# Fetch 24hr ticker data
def fetch_ticker_data(symbol):
    response = requests.get(TICKER_URL, params={"symbol": symbol})
    return response.json()

# Fetch historical kline/candlestick data
def fetch_klines(symbol, interval='1m', limit=100):
    response = requests.get(KLINE_URL, params={"symbol": symbol, "interval": interval, "limit": limit})
    return response.json()

# Calculate RSI
def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period + 1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down
    rsi = 100 - (100 / (1 + rs))

    for i in range(period + 1, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0
        else:
            upval = 0
            downval = -delta

        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down
        rsi = np.append(rsi, 100 - (100 / (1 + rs)))

    return rsi

# Calculate Moving Average
def calculate_moving_average(prices, window=20):
    return np.convolve(prices, np.ones(window), 'valid') / window

# Calculate MACD
def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
    short_ema = calculate_moving_average(prices, window=short_window)
    long_ema = calculate_moving_average(prices, window=long_window)
    
    # Ensure both arrays have the same length
    min_length = min(len(short_ema), len(long_ema))
    short_ema = short_ema[-min_length:]
    long_ema = long_ema[-min_length:]
    
    macd = short_ema - long_ema
    signal = calculate_moving_average(macd, window=signal_window)
    
    # Ensure MACD and Signal have the same length
    min_length = min(len(macd), len(signal))
    macd = macd[-min_length:]
    signal = signal[-min_length:]
    
    return macd, signal

# Strategy 1: RSI-Based Scalping
def rsi_strategy(rsi):
    if rsi < 30:
        return "Buy (Oversold)"
    elif rsi > 70:
        return "Sell (Overbought)"
    else:
        return "Hold"

# Strategy 2: Moving Average Crossover
def ma_crossover_strategy(short_ma, long_ma):
    if short_ma[-1] > long_ma[-1]:
        return "Buy (Uptrend)"
    else:
        return "Sell (Downtrend)"

# Strategy 3: MACD Crossover
def macd_strategy(macd, signal):
    if macd[-1] > signal[-1]:
        return "Buy (Bullish Crossover)"
    else:
        return "Sell (Bearish Crossover)"

# Price Prediction using Linear Regression
def predict_price(prices):
    X = np.arange(len(prices)).reshape(-1, 1)  # Time steps as features
    y = prices  # Prices as target
    model = LinearRegression()
    model.fit(X, y)
    next_price = model.predict([[len(prices)]])[0]
    return next_price

# Main function to test strategies
def test_strategies(symbol):
    # Fetch data
    ticker_data = fetch_ticker_data(symbol)
    klines = fetch_klines(symbol)

    # Extract closing prices
    closing_prices = np.array([float(kline[4]) for kline in klines])

    # Calculate indicators
    rsi = calculate_rsi(closing_prices)
    short_ma = calculate_moving_average(closing_prices, window=10)
    long_ma = calculate_moving_average(closing_prices, window=20)
    macd, signal = calculate_macd(closing_prices)

    # Generate signals
    rsi_signal = rsi_strategy(rsi[-1])
    ma_signal = ma_crossover_strategy(short_ma, long_ma)
    macd_signal = macd_strategy(macd, signal)

    # Predict next price
    next_price = predict_price(closing_prices)

    # Display results
    print(f"Token: {symbol}")
    print(f"Current Price: {ticker_data['lastPrice']}")
    print(f"24h High: {ticker_data['highPrice']}")
    print(f"24h Low: {ticker_data['lowPrice']}")
    print(f"24h Volume: {ticker_data['volume']}")
    print(f"Price Change %: {ticker_data['priceChangePercent']}%")
    print("\nStrategy Results:")
    print(f"RSI Strategy: {rsi_signal} (RSI: {rsi[-1]:.2f})")
    print(f"MA Crossover Strategy: {ma_signal}")
    print(f"MACD Strategy: {macd_signal}")
    print(f"Predicted Next Price: {next_price:.2f}")
    print("-" * 50)

    # Final Opinion
    current_price = float(ticker_data['lastPrice'])
    if next_price > current_price:
        print("Final Opinion: Bullish (Predicted Price > Current Price)")
    else:
        print("Final Opinion: Bearish (Predicted Price <= Current Price)")
    print("=" * 50)

# Test cases
if __name__ == "__main__":
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Add more tokens if needed
    for symbol in symbols:
        test_strategies(symbol)
        time.sleep(1)  # Avoid rate limits