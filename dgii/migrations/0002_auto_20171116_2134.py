# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgii', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marbete',
            name='penalized',
            field=models.BooleanField(default=False),
        ),
    ]