# Generated by Django 3.0.2 on 2020-03-16 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='tur_oprettet',
            field=models.CharField(default="[{'0':'0', '1':'0', '2':'0', '3':'0'}]", max_length=50),
        ),
    ]
