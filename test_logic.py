import yfinance as yf
import pandas as pd
from pypfopt import HRPOpt

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"]
START_DATE = (pd.Timestamp.now() - pd.DateOffset(years=2)).strftime('%Y-%m-%d')
END_DATE = pd.Timestamp.now().strftime('%Y-%m-%d')

print("Fetching data...")
try:
    data = yf.download(TICKERS, start=START_DATE, end=END_DATE, auto_adjust=True, progress=False)
    # Basic clean up logic to mimic app.py
    if hasattr(data, "columns") and isinstance(data.columns, pd.MultiIndex):
            if 'Close' in data.columns.get_level_values(0):
                data = data['Close']
            elif 'Adj Close' in data.columns.get_level_values(0):
                data = data['Adj Close']
    
    print(f"Data shape: {data.shape}")
    if data.empty:
        print("Data is empty!")
        exit(1)
        
    print("Running HRP...")
    returns = data.pct_change().dropna()
    optimizer = HRPOpt(returns)
    weights = optimizer.optimize()
    print("Optimization successful!")
    print("Weights:", weights)
    
    perf = optimizer.portfolio_performance(verbose=True)
    print("Performance:", perf)

except Exception as e:
    print(f"FAILED: {e}")
    exit(1)
