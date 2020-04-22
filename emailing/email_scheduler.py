import requests

r = requests.get("http://kacaring.pythonanywhere.com/email/check_scheduler")
print(r)