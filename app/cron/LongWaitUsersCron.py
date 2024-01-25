from django_cron import CronJobBase, Schedule
import requests

class LongWaitUsersCron(CronJobBase):
    # RUN_AT_TIMES = ['14:10']
    RUN_EVERY_MINS = 1

    # schedule = Schedule(run_at_times=RUN_AT_TIMES)
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.long_wait_users_cron'    # a unique code

    def do(self):
        requests.get('http://127.0.0.1:8000/')
        print('LongWaitUsersCron')
        pass    # do your thing here
