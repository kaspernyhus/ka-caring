from django.db import models

class UserPreferences(models.Model):
  monthly_saldo = models.CharField(max_length=50, default="[{'0':'0', '1':'0', '2':'0', '3':'0'}]")
  udgift_oprettet = models.CharField(max_length=50, default="[{'0':'0', '1':'0', '2':'0', '3':'0'}]")
  tankning_oprettet = models.CharField(max_length=50, default="[{'0':'0', '1':'0', '2':'0', '3':'0'}]")
  tur_oprettet = models.CharField(max_length=50, default="[{'0':'0', '1':'0', '2':'0', '3':'0'}]")


class EmailQue(models.Model):
  email_que = models.CharField(max_length=5000, default="[]")