# Generated by Django 3.0.2 on 2020-01-30 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ture', '0002_ture_delta_km'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ture',
            name='delta_km',
            field=models.IntegerField(),
        ),
    ]