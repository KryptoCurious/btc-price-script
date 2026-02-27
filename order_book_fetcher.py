# Project 4: Fetch and display order book (bids & asks) for crypto pairs
# Shows top levels — useful for understanding market depth & market making

import ccxt
import time

# Connect to Binance (public data)
exchange = ccxt.binance()

# Pairs to check (start with one, easy to expand)
pairs = ['BTC/USDT']  # Add more later: 'ETH/USDT', 'SOL/USDT', etc.

# How many levels to show on each side (bids/asks)
depth_levels = 10

print("=== Order Book Fetcher Started ===")
print(f"Showing top {depth_levels} levels per side\n")

try:
    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{current_time}] Order Book Snapshot ───────────────────────────────")

        for pair in pairs:
            try:
                # Fetch order book (limit = number of levels)
                orderbook = exchange.fetch_order_book(pair, limit=depth_levels)

                bids = orderbook['bids']      # [price, quantity] descending
                asks = orderbook['asks']      # [price, quantity] ascending

                mid_price = (bids[0][0] + asks[0][0]) / 2 if bids and asks else None
                spread = asks[0][0] - bids[0][0] if bids and asks else None

                print(f"\n{pair} (Mid: ${mid_price:,.2f} | Spread: ${spread:,.2f})")

                print("  Bids (Buyers - highest first)          Asks (Sellers - lowest first)")
                print("  Price       Qty     Cum Qty          Price       Qty     Cum Qty")

                cum_bid_qty = 0
                cum_ask_qty = 0

                for i in range(depth_levels):
                    bid_price, bid_qty = bids[i] if i < len(bids) else (None, None)
                    ask_price, ask_qty = asks[i] if i < len(asks) else (None, None)

                    cum_bid_qty += bid_qty if bid_qty else 0
                    cum_ask_qty += ask_qty if ask_qty else 0

                    bid_str = f"${bid_price:,.2f}  {bid_qty:>8.2f}  {cum_bid_qty:>8.2f}" if bid_price else "—"
                    ask_str = f"${ask_price:,.2f}  {ask_qty:>8.2f}  {cum_ask_qty:>8.2f}" if ask_price else "—"

                    print(f"  {bid_str:<35} {ask_str}")

            except Exception as e:
                print(f"Error fetching {pair}: {str(e)[:80]}...")

        print("=" * 70)
        time.sleep(30)  # Refresh every 30 seconds (Binance allows ~1200 req/min)

except KeyboardInterrupt:
    print("\nOrder book fetcher stopped. Goodbye!")
except Exception as e:
    print(f"Unexpected error: {e}")