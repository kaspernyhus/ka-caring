# Generated by Django 3.0.2 on 2020-01-27 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('km', models.IntegerField(blank=True)),
                ('user_id', models.IntegerField(blank=True)),
            ],
        ),
    ]