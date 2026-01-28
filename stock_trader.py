import alpaca_trade_api as tradeapi
from collections import deque
import random

api = tradeapi.REST('AKCIP6PBVKIJJ43ZLLEDIGJ6L5', 'AKtJwbNCZpjbERLrcHmwdhMB1hC1uREjokeyq2de1nvz',
base_url = 'https://api.alpaca.markets',
api_version = 'v2')

#Checks balance of user's account on Alpaca
def check_balance():
    try:
        account = api.get_account()
        print(f"Cash: ${account.cash}")
        print(f"Buying Power: ${account.buying_power}")
        print(f"Equity: ${account.equity}")
        return account
    except Exception as e:
        print(f"Error checking balance: {e}")

def get_stock_price(symbol):
    try:
        quote = api.get_latest_quote(symbol)
        return float(quote.ap)
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

#Submits order to Alpaca
def submit_order(symbol, qty, side, order_type = 'market'):
    try:
        order = api.submit_order(symbol = symbol, qty = qty, side = side, type = order_type, time_in_force = 'gtc')
        print(f"Submitted {order_type} {side} order for {qty} shares of {symbol}")
        return order
    except Exception as e:
        print(f"Order failed: {e}")
        return None

#Function to simulate trade
def simulate_trade(symbol, qty, action):
    print("\n== Trade Simulation ===")

    print("\n[1/4] Account Balance:")
    account = check_balance()
    if not account:
        return

    print(f"\n[2/4] Checking {symbol} price:")
    price = get_stock_price(symbol)
    if not price:
        return
    print(f"Current {symbol} price: ${price:.2f}")

    print(f"\n[3/4] Submitting {action} order:")
    order = submit_order(symbol, qty, action)
    if not order:
        return
    
    print("\n[4/4] Order Status: ")
    try:
        order_status = api.get_order(order.id)
        print(f"Status: {order_status.status}")
        print(f"Filled Qty: {order_status.filled_qty}")
        print(f"Average Fill Price: ${order_status.filled_avg_price or 'N/A'}")
    except Exception as e:
        print(f"Error checking order status: {e}")



        

if __name__ == "__main__":
    # Get user input and run function for simulating trade for buy/sell, or just check positions
    action = input("buy, sell, or check? ").lower()
   
   #If statement for necessary user input
    if action == 'buy':
        company = input("Enter a ticker symbol: ")
        shares = int(input("How many shares? "))
        simulate_trade(company, shares, 'buy')
    elif action == 'sell':
        company = input("Enter a ticker symbol: ")
        shares = int(input("How many shares? "))
        simulate_trade(company, shares, 'sell')
    #Do nothing if user wants to check positions
    elif action == 'check':
        pass
    else:
        print("Invalid, please try again: ")
    
    # Check portfolio after trade
    try:
        positions = api.list_positions()
        print("\n=== Current Positions ===")
        for position in positions:
            print(f"{position.symbol}: {position.qty} shares")
    except Exception as e:
        print(f"Error checking positions: {e}")

#Function for automating trade
def execute_auto_trade(signal):
    #The ticker, symbol, and action saved to one variable
    symbol = signal["ticker"]
    action = signal["action"]


    # Get current position 
    try:
        position = api.get_position(symbol)
        current_qty = float(position.qty)
    except Exception:  # No position exists
        current_qty = 0
    
    # Prevent selling if there are no shares
    if action == "sell" and current_qty <= 0:
        print(f"Cannot sell {symbol}: No shares held (Qty: {current_qty})")
        return
    
    #Return trade info if trade is successful
    return simulate_trade (
        symbol = signal["ticker"],
        qty = random.randint(1, 20),
        action = signal["action"],
    )
  