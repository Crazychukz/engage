# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-05-15 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engage', '0030_auto_20190515_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='nursery_population',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Nursery Population'),
        ),
    ]
