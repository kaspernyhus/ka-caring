# Generated by Django 3.0.2 on 2020-04-05 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='betaling',
            name='is_indskud',
            field=models.BooleanField(blank=True, default=0),
        ),
    ]