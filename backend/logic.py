import yfinance as yf
import pandas as pd
import numpy as np
from pypfopt import HRPOpt
import database

# Configuration
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "SPY"]
LOOKBACK_YEARS = 2

def update_market_data():
    """
    Downloads latest data for tickers and saves to DB. as append only.
    Ideally we fetch the last 2 years again to fill gaps/corrections, or just last few days.
    For simplicity and robustness, we fetch full 2 years to ensure we have the window.
    """
    print("Updating market data...")
    start_date = (pd.Timestamp.now() - pd.DateOffset(years=LOOKBACK_YEARS)).strftime('%Y-%m-%d')
    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    
    try:
        data = yf.download(TICKERS, start=start_date, end=end_date, auto_adjust=True, progress=False)
        
        # Cleanup MultiIndex if present
        if hasattr(data, "columns") and isinstance(data.columns, pd.MultiIndex):
             if 'Close' in data.columns.get_level_values(0):
                 data = data['Close']
             elif 'Adj Close' in data.columns.get_level_values(0):
                 data = data['Adj Close']
        
        if not data.empty:
            database.save_prices(data)
            print("Market data updated.")
            return True
    except Exception as e:
        print(f"Error updating data: {e}")
        return False
    return False

def rebalance_portfolio_if_needed():
    """
    Checks if we have an allocation for today (or recent enough).
    If not, runs HRP and saves it.
    """
    # 1. Check last allocation
    latest = database.get_latest_allocation()
    today_str = pd.Timestamp.now().strftime('%Y-%m-%d')
    
    force_rebalance = False
    
    if latest:
        last_date = latest['date']
        print(f"Last allocation date: {last_date}")
        # Simple Logic: Rebalance if last allocation is not from this month (Monthly)
        # Or Just Weekly. Let's do: If last allocation is older than 7 days.
        days_diff = (pd.Timestamp(today_str) - pd.Timestamp(last_date)).days
        if days_diff >= 7:
            print(f"Allocation is {days_diff} days old. Rebalancing...")
            force_rebalance = True
        else:
            print("Allocation is fresh. No rebalance needed.")
    else:
        print("No allocation found. Initial rebalance.")
        force_rebalance = True

    if force_rebalance:
        # Load prices from DB
        df = database.get_prices()
        if df.empty:
            print("Not enough data to rebalance.")
            return

        # Exclude SPY from optimization universe
        opt_tickers = [t for t in TICKERS if t != "SPY"]
        portfolio_prices = df[opt_tickers].dropna()
        
        if portfolio_prices.empty:
            print("Not enough data for portfolio tickers.")
            return

        # Run HRP
        try:
            returns = portfolio_prices.pct_change().dropna()
            optimizer = HRPOpt(returns)
            weights = optimizer.optimize()
            perf = optimizer.portfolio_performance(verbose=False, risk_free_rate=0.02)
            
            # Perf comes as (return, vol, sharpe)
            metrics = {
                "expected_return": perf[0],
                "volatility": perf[1],
                "sharpe_ratio": perf[2]
            }
            
            database.save_allocation(weights, metrics)
            print("New allocation saved!")
            
        except Exception as e:
            print(f"Optimization failed: {e}")
