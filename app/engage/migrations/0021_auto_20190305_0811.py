# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-03-05 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engage', '0020_auto_20190227_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='kelloggsschool',
            name='branch',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Branch'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='mc_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='MC Name'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='visit_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Visit End Date'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='visit_end_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Visit End Time'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='visit_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Visit Start Date'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='visit_start_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Visit Start Time'),
        ),

    ]
