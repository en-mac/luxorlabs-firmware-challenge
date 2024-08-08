from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from utils import get_current_time_period
from apscheduler.triggers.interval import IntervalTrigger

import time

class Scheduler:
    def __init__(self, miner_controller, miners, state):
        self.miner_controller = miner_controller
        self.miners = miners
        self.state = state
        self.current_period = get_current_time_period()
        self.scheduler = BackgroundScheduler()
        self.schedule_jobs()
        self.scheduler.start()

    def schedule_jobs(self):
        # Schedule jobs at specified times
        self.scheduler.add_job(self.run, CronTrigger(hour=0, minute=0))
        self.scheduler.add_job(self.run, CronTrigger(hour=6, minute=0))
        self.scheduler.add_job(self.run, CronTrigger(hour=12, minute=0))
        self.scheduler.add_job(self.run, CronTrigger(hour=18, minute=0))
        # Perform initial update immediately
        self.run()

    # ## TESTING#
    # def schedule_jobs(self):
    #     # Schedule jobs to run every 5 seconds for testing
    #     self.scheduler.add_job(self.run, IntervalTrigger(seconds=15))
    #     # Perform initial update immediately
    #     self.run()


    def run(self):
        new_period = get_current_time_period()
        for miner_ip in self.miners:
            try:
                login_attempt = self.miner_controller.login(miner_ip)
                print("Login attempt: ", login_attempt)
                profile, state = self.miner_controller.update_miner_mode(miner_ip)
                self.state[miner_ip] = {
                    "token": self.miner_controller.tokens[miner_ip],
                    "profile": profile,
                    "state": state
                }
            except Exception as e:
                print(f"Failed to update miner {miner_ip}: {e}")

    def start(self):
        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()
