# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-16 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_userlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='loc_type',
            field=models.CharField(default='user', max_length=250),
        ),
        migrations.AddField(
            model_name='location',
            name='type_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]