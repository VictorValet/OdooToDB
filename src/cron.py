import odooToDB
import signal
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(odooToDB.odooToDB, 'interval', seconds=30)
scheduler.start()

def exit(signum, frame):
    print("Shutting down cron job...")
    scheduler.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        exit(None, None)
