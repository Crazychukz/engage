# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-03-05 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engage', '0021_auto_20190305_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='kelloggsschool',
            name='final_lat',
            field=models.FloatField(default=0.0, null=True, verbose_name='Final Latitude'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='final_lng',
            field=models.FloatField(default=0.0, null=True, verbose_name='Final Longitude'),
        ),
    ]