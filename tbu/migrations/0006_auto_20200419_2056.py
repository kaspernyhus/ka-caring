# Generated by Django 3.0.2 on 2020-04-19 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbu', '0005_auto_20200405_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='betaling',
            name='description',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='betaling',
            name='is_indskud',
            field=models.BooleanField(blank=True),
        ),
    ]
