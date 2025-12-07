import database
import logic
import sys

def main():
    print("--- Starting Portfolio Updater ---")
    
    # 1. Init DB if not exists
    print("Initializing Database...")
    database.init_db()
    
    # 2. Update Market Data
    print("Fetching Market Data...")
    success = logic.update_market_data()
    if not success:
        print("Market data update failed. Continuing to rebalance check might be risky, but trying anyway...")
    
    # 3. Rebalance
    print("Checking Rebalance Rules...")
    logic.rebalance_portfolio_if_needed()
    
    print("--- Update Complete ---")

if __name__ == "__main__":
    main()
