import time
import schedule
import logic
from datetime import datetime
import os
import sys

# Ensure we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def job():
    print(f"[{datetime.now()}] Running scheduled update...")
    logic.update_market_data()
    logic.rebalance_portfolio_if_needed()

print("--- Scheduler Started ---")
# Run once on startup
try:
    job()
except Exception as e:
    print(f"Error executing initial job: {e}")

schedule.every().day.at("22:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
