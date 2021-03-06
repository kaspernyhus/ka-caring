# Generated by Django 3.0.2 on 2020-04-05 13:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0015_auto_20200403_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Udgift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField()),
                ('description', models.CharField(max_length=200)),
                ('user_id', models.CharField(max_length=50)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.TransactionId')),
            ],
            options={
                'verbose_name_plural': 'Udgifter',
            },
        ),
        migrations.CreateModel(
            name='Tankning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField()),
                ('user_id', models.CharField(max_length=50)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.TransactionId')),
            ],
            options={
                'verbose_name_plural': 'Tankninger',
            },
        ),
        migrations.CreateModel(
            name='Betaling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField()),
                ('user_id', models.CharField(max_length=50)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.TransactionId')),
            ],
            options={
                'verbose_name_plural': 'Betalinger',
            },
        ),
    ]
