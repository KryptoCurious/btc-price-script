# Here is my Second Project 2 : Live monitor for multiple cryptocurrencies
# Prints updated prices every 30 seconds for a list of coins

import ccxt
import time

# Connect to Binance (public data only)
exchange = ccxt.binance()

# List of pairs to monitor 
pairs = [
    'BTC/USDT',
    'ETH/USDT',
    'SOL/USDT',
    'BNB/USDT',
    'XRP/USDT',
    'ADA/USDT',
    #'DOGE/USDT',   # i can add more 
    #'TON/USDT',
]

print("=== Multi-Coin Live Monitor Started ===")
print(f"Watching {len(pairs)} pairs: {', '.join(pairs)}")
print("Updates every 30 seconds. Press Ctrl+C to stop\n")

try:
    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{current_time}] ────────────────────────────────────────")

        for pair in pairs:
            try:
                ticker = exchange.fetch_ticker(pair)
                price = ticker['last']
                change_24h = ticker['percentage']   # 24h % change
                volume_24h = ticker['quoteVolume']

                change_str = f"{change_24h:+.2f}%" if change_24h is not None else "N/A"
                print(f"  {pair:10} | ${price:,.2f} | 24h: {change_str:>7} | Vol: {volume_24h:,.0f} USDT")

            except Exception as e:
                print(f"  {pair:10} | Error: {e}")

        print("-" * 60)
        time.sleep(30)  # Wait 30 seconds

except KeyboardInterrupt:
    print("\nMonitor stopped by user. Goodbye!")
except Exception as e:
    print(f"Unexpected error: {e}")