from django.db import models
from datetime import date


class Tankning(models.Model):
    date = models.DateField(default=date.today)
    amount = models.FloatField()
    user_id = models.CharField(max_length=50)


class Betaling(models.Model):
    date = models.DateField(default=date.today)
    amount = models.FloatField()
    user_id = models.CharField(max_length=50)


class Udgift(models.Model):
    date = models.DateField(default=date.today)
    amount = models.FloatField()
    description = models.CharField(max_length=200)
    user_id = models.CharField(max_length=50)