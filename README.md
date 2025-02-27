# crypto-bot
``` bash
 docker build -t crypto-bot .
 docker run -v bot crypto-bot
 ```
# Sample OutPut:
```
Token: BTCUSDT
Current Price: 84282.83000000
24h High: 87078.46000000
24h Low: 82716.49000000
24h Volume: 45101.11132000
Price Change %: 0.153%

Strategy Results:
RSI Strategy: Hold (RSI: 61.65)
MA Crossover Strategy: Buy (Uptrend)
MACD Strategy: Buy (Bullish Crossover)
Predicted Next Price: 84063.35
--------------------------------------------------
Final Opinion: Bearish (Predicted Price <= Current Price)
==================================================
Token: ETHUSDT
Current Price: 2275.92000000
24h High: 2383.37000000
24h Low: 2230.57000000
24h Volume: 663040.42180000
Price Change %: -1.765%

Strategy Results:
RSI Strategy: Hold (RSI: 66.05)
MA Crossover Strategy: Buy (Uptrend)
MACD Strategy: Buy (Bullish Crossover)
Predicted Next Price: 2255.38
--------------------------------------------------
Final Opinion: Bearish (Predicted Price <= Current Price)
==================================================
Token: BNBUSDT
Current Price: 603.51000000
24h High: 619.77000000
24h Low: 595.84000000
24h Volume: 311628.55400000
Price Change %: -0.665%

Strategy Results:
RSI Strategy: Hold (RSI: 64.63)
MA Crossover Strategy: Buy (Uptrend)
MACD Strategy: Sell (Bearish Crossover)
Predicted Next Price: 600.85
--------------------------------------------------
Final Opinion: Bearish (Predicted Price <= Current Price)
```