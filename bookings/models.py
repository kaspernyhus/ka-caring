from django.db import models
from django.contrib import admin 
from django.contrib.auth.models import User 
from oauth2client.contrib.django_util.models import CredentialsField 


class CredentialsModel(models.Model):
	credential = CredentialsField()


class CredentialsAdmin(admin.ModelAdmin): 
	pass
