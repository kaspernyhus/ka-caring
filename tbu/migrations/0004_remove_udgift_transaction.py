# Generated by Django 3.0.2 on 2020-02-01 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbu', '0003_auto_20200201_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='udgift',
            name='transaction',
        ),
    ]