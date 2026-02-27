# Project 4 upgraded: Multi-coin order book fetcher
# Shows top bids/asks, mid-price, spread for multiple pairs

import ccxt
import time

# Connect to Binance (public data only)
exchange = ccxt.binance()

# Same top coins list from previous projects
pairs = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT',
    'USDC/USDT', 'DOGE/USDT', 'ADA/USDT', 'AVAX/USDT', 'SHIB/USDT',
    'LINK/USDT', 'TRX/USDT', 'DOT/USDT', 'TON/USDT', 'MATIC/USDT',
    'LTC/USDT', 'BCH/USDT', 'NEAR/USDT', 'UNI/USDT', 'PEPE/USDT'
]

# How many levels to show per side (keeping small for readability)
depth_levels = 5

print("=== Multi-Coin Order Book Fetcher Started ===")
print(f"Watching {len(pairs)} pairs | Top {depth_levels} levels per side")
print("Updates every 60 seconds. Press Ctrl+C to stop.\n")

try:
    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{current_time}] Multi Order Book Snapshot ───────────────────────────────")

        for pair in pairs:
            try:
                # Fetch order book with limited depth
                orderbook = exchange.fetch_order_book(pair, limit=depth_levels)

                bids = orderbook['bids']  # list of [price, qty], highest buy first
                asks = orderbook['asks']  # lowest sell first

                if not bids or not asks:
                    print(f"  {pair:12} | No order book data available")
                    continue

                best_bid = bids[0][0]
                best_ask = asks[0][0]
                mid_price = (best_bid + best_ask) / 2
                spread = best_ask - best_bid
                spread_pct = (spread / mid_price) * 100 if mid_price > 0 else 0

                print(f"\n{pair}")
                print(f"  Mid Price: ${mid_price:,.2f} | Spread: ${spread:,.2f} ({spread_pct:.3f}%)")

                print("  Bids (highest first)                  Asks (lowest first)")
                print("  Price      Qty      Cum            Price      Qty      Cum")

                cum_bid = 0
                cum_ask = 0

                for i in range(depth_levels):
                    bid_p, bid_q = bids[i] if i < len(bids) else (None, None)
                    ask_p, ask_q = asks[i] if i < len(asks) else (None, None)

                    cum_bid += bid_q if bid_q else 0
                    cum_ask += ask_q if ask_q else 0

                    bid_line = f"${bid_p:,.2f}  {bid_q:>6.2f}  {cum_bid:>6.2f}" if bid_p else "—"
                    ask_line = f"${ask_p:,.2f}  {ask_q:>6.2f}  {cum_ask:>6.2f}" if ask_p else "—"

                    print(f"  {bid_line:<32} {ask_line}")

            except Exception as e:
                print(f"  {pair:12} | Error: {str(e)[:70]}...")

        print("=" * 80 + "\n")
        time.sleep(60)  # 60 seconds - safer for many pairs

except KeyboardInterrupt:
    print("\nMulti order book fetcher stopped. Goodbye!")
except Exception as e:
    print(f"Unexpected error: {e}")