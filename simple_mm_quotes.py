# Project 5: Simple market-making quote generator with inventory skew
# Fetches real mid-price/spread → generates skewed quotes based on inventory

import ccxt
import time

# Connect to Binance
exchange = ccxt.binance()

# Pair to simulate (easy to change or loop multiple)
pair = 'BTC/USDT'

# Simulation parameters (tweak these!)
base_spread_pct = 0.05      # Desired neutral spread as % of mid (e.g. 0.05% = very tight)
skew_factor = 0.30          # How aggressively to skew (0.0 = no skew, 1.0 = full skew)
max_inventory = 0.5         # Max BTC position before full skew (e.g. 0.5 BTC)
quote_size = 0.01           # Simulated quote quantity (BTC)

# Current simulated inventory (positive = long BTC, negative = short)
# Change this manually to test different scenarios
inventory = 0.2             # Example: mildly long

print("=== Simple Market-Making Quote Simulator Started ===")
print(f"Pair: {pair} | Base spread: {base_spread_pct}% | Skew factor: {skew_factor}")
print(f"Inventory: {inventory:+.4f} BTC | Max inv: ±{max_inventory} BTC\n")

try:
    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{current_time}] Quote Generation ───────────────────────────────")

        try:
            # Fetch real order book (top level only needed)
            orderbook = exchange.fetch_order_book(pair, limit=1)

            best_bid = orderbook['bids'][0][0] if orderbook['bids'] else None
            best_ask = orderbook['asks'][0][0] if orderbook['asks'] else None

            if best_bid is None or best_ask is None:
                print("  No valid order book data")
                time.sleep(30)
                continue

            mid_price = (best_bid + best_ask) / 2
            real_spread = best_ask - best_bid
            real_spread_pct = (real_spread / mid_price) * 100

            # Calculate desired neutral half-spread
            half_spread = mid_price * (base_spread_pct / 100) / 2

            # Inventory skew adjustment
            # Normalize inventory: -1 (max short) to +1 (max long)
            inv_normalized = inventory / max_inventory
            inv_normalized = max(min(inv_normalized, 1.0), -1.0)  # clamp

            # Skew: positive inv → lower ask (sell cheaper), raise bid (buy higher)
            skew_adjust = inv_normalized * skew_factor * half_spread

            sim_bid = mid_price - half_spread + skew_adjust
            sim_ask = mid_price + half_spread + skew_adjust

            sim_spread = sim_ask - sim_bid

            print(f"  Real Mid:     ${mid_price:,.2f}")
            print(f"  Real Spread:  ${real_spread:,.2f} ({real_spread_pct:.3f}%)")
            print(f"  Inventory:    {inventory:+.4f} BTC (skew: {inv_normalized:+.2%})")
            print("")
            print(f"  Simulated Bid:  ${sim_bid:,.2f}   size: {quote_size:.4f} BTC")
            print(f"  Simulated Ask:  ${sim_ask:,.2f}   size: {quote_size:.4f} BTC")
            print(f"  Sim Spread:     ${sim_spread:,.2f} ({(sim_spread/mid_price*100):.3f}%)")

        except Exception as e:
            print(f"  Error: {str(e)[:80]}...")

        print("=" * 60 + "\n")
        time.sleep(30)

except KeyboardInterrupt:
    print("\nSimulator stopped. Goodbye!")
except Exception as e:
    print(f"Unexpected error: {e}")