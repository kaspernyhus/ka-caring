# Generated by Django 3.0.2 on 2020-03-11 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200311_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='onbankaccount',
            name='description',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
