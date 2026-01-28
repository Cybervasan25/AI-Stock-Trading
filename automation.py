#from news_headlines import get_trade_signals
#from stock_trader import execute_auto_trade
import news_headlines as nh
import stock_trader as st
import alpaca_trade_api as tradeapi
import time

api = tradeapi.REST(
    'APCA_API_KEY_ID',
    'APCA_API_SECRET_KEY',
    base_url='https://api.alpaca.markets'  
)



#Function for checking if account has sufficient funds to buy
def has_sufficient_funds(symbol, qty):
    """Check if account has enough buying power for the trade."""
    try:
        account = api.get_account()
        buying_power = float(account.buying_power)
        current_price = float(api.get_latest_trade(symbol).price)
        total_cost = current_price * qty

        if total_cost > buying_power:
            print(f"Insufficient funds for {qty} {symbol}. Needed: ${total_cost:.2f}, Available: ${buying_power:.2f}")
            return False
        return True

    except Exception as e:
        print(f"⚠️ Funds check error: {e}")
        return False

def main():
    while True:
        print("\n==Running Trades==")

        #Gets trade suggestions from news_headlines
        signals = nh.get_trade_signals()

        #Executes trade based on suggestions 
        for signal in signals:
            st.execute_auto_trade(signal)

        #Wait for few minutes before next trade cycle
        time.sleep(600)

if __name__ == "__main__":
    main()