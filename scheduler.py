import time
import schedule
import updater
from datetime import datetime

def job():
    print(f"[{datetime.now()}] Running scheduled update...")
    updater.main()

# Schedule the job every day at 22:00 (10 PM)
# Or for testing, we can run it on startup
# Let's run it once on startup to be safe, then schedule.
print("--- Scheduler Started ---")
job()

schedule.every().day.at("22:00").do(job)
# Also every weekday just in case
# schedule.every().monday.at("22:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
