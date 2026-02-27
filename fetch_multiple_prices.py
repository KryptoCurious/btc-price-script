# Project 1: Fetch prices for multiple cryptocurrencies using ccxt
# Shows current price, 24h high/low, volume for several coins

import ccxt
import time

# Connect to Binance (public data only - no keys needed)
exchange = ccxt.binance()

# List of trading pairs we want to check
pairs = [
    'BTC/USDT',
    'ETH/USDT',
    'SOL/USDT',
    'BNB/USDT',
    'XRP/USDT'
]

print("=== Multi-Coin Price Update ===")
print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

for pair in pairs:
    try:
        ticker = exchange.fetch_ticker(pair)
        
        print(f"📊 {pair}")
        print(f"  Current Price: ${ticker['last']:.4f}")
        print(f"  24h High:      ${ticker['high']:.4f}")
        print(f"  24h Low:       ${ticker['low']:.4f}")
        print(f"  24h Volume:    {ticker['quoteVolume']:,.2f} USDT")
        print("-" * 40)
        
    except Exception as e:
        print(f"Error fetching {pair}: {e}")
        print("-" * 40)

print("Done!")