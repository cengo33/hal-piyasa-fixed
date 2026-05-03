import os
import time
import schedule
from auto_post import run_auto_post

def job():
    print("Executing scheduled task...")
    run_auto_post()

if __name__ == "__main__":
    print("Starting TikTok Facebook Poster Worker (Runs every 6 hours)")
    
    # Run once at startup
    job()
    
    # Schedule every 6 hours
    schedule.every(6).hours.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
