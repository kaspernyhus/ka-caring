import requests
import datetime

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

today = datetime.datetime.now()
ldom = last_day_of_month(today.date())


if today.date() == ldom:
    print('-------------- Emails send ----------------')
    r = requests.get("http://kacaring.pythonanywhere.com/email/send")
    print(r)