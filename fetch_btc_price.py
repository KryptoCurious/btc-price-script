# Simple script to fetch live BTC/USDT price using ccxt
# Just Curiously Uploading my first project for crypto quant learning!

import ccxt

# Connect to Binance (no API keys needed for public data)
exchange = ccxt.binance()

# Fetch the ticker (current price info)
ticker = exchange.fetch_ticker('BTC/USDT')

# Print key info
print("=== BTC/USDT on Binance ===")
print(f"Current Price: ${ticker['last']:.2f}")
print(f"24h High: ${ticker['high']:.2f}")
print(f"24h Low: ${ticker['low']:.2f}")
print(f"24h Volume: {ticker['quoteVolume']:.2f} USDT")
print(f"Last Updated: {ticker['datetime']}")