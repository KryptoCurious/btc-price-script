# Project 3: Log top crypto prices to CSV file every 30 seconds
# Saves timestamp + prices for multiple coins → open in Excel/Google Sheets

import ccxt
import time
import csv
import os

# Connect to Binance
exchange = ccxt.binance()

# Top ~20 pairs (edit as needed)
pairs = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT',
    'USDC/USDT', 'DOGE/USDT', 'ADA/USDT', 'AVAX/USDT', 'SHIB/USDT',
    'LINK/USDT', 'TRX/USDT', 'DOT/USDT', 'TON/USDT', 'MATIC/USDT',
    'LTC/USDT', 'BCH/USDT', 'NEAR/USDT', 'UNI/USDT', 'PEPE/USDT'
]

# CSV file name (will be created on Desktop if not exists)
csv_file = 'crypto_prices.csv'

# Headers (only written once if file is new)
headers = ['Timestamp'] + pairs  # e.g., Timestamp, BTC/USDT, ETH/USDT, ...

# Check if file exists → if not, write headers
file_exists = os.path.isfile(csv_file)

print(f"=== Price Logger to CSV Started ===")
print(f"Saving data every 30 seconds to: {csv_file}")
print(f"Watching {len(pairs)} pairs. Press Ctrl+C to stop.\n")

try:
    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        row = [current_time]  # Start with timestamp

        print(f"[{current_time}] Fetching prices...")

        for pair in pairs:
            try:
                ticker = exchange.fetch_ticker(pair)
                price = ticker['last']
                row.append(price)  # Add price to row

                print(f"  {pair:12} → ${price:,.4f}")

            except Exception as e:
                print(f"  {pair:12} → Error: {str(e)[:50]}...")
                row.append(None)  # Or 'Error' - None is better for analysis

        # Write the row to CSV
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)  # Write headers only first time
                file_exists = True  # Prevent rewriting headers
            writer.writerow(row)

        print(f"Row saved. Waiting 30 seconds...\n")
        time.sleep(30)

except KeyboardInterrupt:
    print("\nLogger stopped by user. Data saved to crypto_prices.csv")
    print("Open the file in Excel or Google Sheets to view your collected prices!")
except Exception as e:
    print(f"Unexpected error: {e}")