import requests

print('-------------- Emails send ----------------')
r = requests.get("http://kacaring.pythonanywhere.com/email/send")
print(r)