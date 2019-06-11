# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-16 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engage', '0015_auto_20181216_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='lga',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='LGA'),
        ),
        migrations.AddField(
            model_name='bar',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='lga',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='LGA'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='lga',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='LGA'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lga',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='LGA'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='State'),
        ),
    ]