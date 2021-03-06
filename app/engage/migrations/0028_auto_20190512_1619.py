# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-05-12 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engage', '0027_auto_20190327_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='kelloggsschool',
            name='cocopops_32g_qty',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Coco Pops 32g'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='cocopops_450g_qty',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Coco Pops 450g'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='dano_cool_cow_25g_qty',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Dano Cool Cow 25g'),
        ),
        migrations.AddField(
            model_name='kelloggsschool',
            name='dano_cool_cow_360g_qty',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Dano Cool Cow 360g'),
        ),

    ]
