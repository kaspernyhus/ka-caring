# Generated by Django 3.0.2 on 2020-03-02 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200302_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kmprice',
            name='price',
            field=models.FloatField(default=2.5),
        ),
    ]
