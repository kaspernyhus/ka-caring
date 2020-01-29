from django.db import models


class Kirsten(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    saldo = models.FloatField()
    km = models.IntegerField()


class Marie(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    saldo = models.FloatField()
    km = models.IntegerField()


class Kasper(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    saldo = models.FloatField()
    km = models.IntegerField()
