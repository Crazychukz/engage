# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-12-09 00:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engage', '0008_auto_20181208_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='date_captured',
            field=models.DateField(blank=True, null=True, verbose_name='Date Captured'),
        ),
        migrations.AddField(
            model_name='bar',
            name='image',
            field=models.ImageField(blank=True, default='horeca/images/noimage.jpg', upload_to='horeca/images/', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='bar',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='engage.UserProfile', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='date_captured',
            field=models.DateField(blank=True, null=True, verbose_name='Date Captured'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='image',
            field=models.ImageField(blank=True, default='horeca/images/noimage.jpg', upload_to='horeca/images/', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='engage.UserProfile', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='date_captured',
            field=models.DateField(blank=True, null=True, verbose_name='Date Captured'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='image',
            field=models.ImageField(blank=True, default='horeca/images/noimage.jpg', upload_to='horeca/images/', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='engage.UserProfile', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='date_captured',
            field=models.DateField(blank=True, null=True, verbose_name='Date Captured'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, default='horeca/images/noimage.jpg', upload_to='horeca/images/', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='engage.UserProfile', verbose_name='User'),
        ),

    ]
