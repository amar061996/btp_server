# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-24 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Location')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.Transport')),
            ],
        ),
    ]
