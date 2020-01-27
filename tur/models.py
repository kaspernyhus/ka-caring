from django.db import models

class Tur(models.Model):
    #Dato = models.DateField(auto_now_add=True, auto_now=False)
    km = models.IntegerField(blank=True)
    user_id = models.IntegerField(blank=True)