from django.db import models
from django.conf import settings


class EmailPreferences(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
  monthly_saldo = models.BooleanField(default=True)
  udgift_oprettet = models.BooleanField(default=False)
  tankning_oprettet = models.BooleanField(default=False)
  tur_oprettet = models.BooleanField(default=False)
  indbetaling_oprettet = models.BooleanField(default=False)


class EmailQue(models.Model):
  email_que = models.CharField(max_length=5000, default="[]")