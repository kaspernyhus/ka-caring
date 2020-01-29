# Generated by Django 3.0.2 on 2020-01-29 14:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Betaling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField()),
                ('user_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tankning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField()),
                ('user_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Udgift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField()),
                ('description', models.CharField(max_length=200)),
                ('user_id', models.CharField(max_length=50)),
            ],
        ),
    ]
