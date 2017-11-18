# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 03:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dgii', '0001_initial'),
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('photo', models.FileField(upload_to='arch')),
                ('fined', models.NullBooleanField(default=False)),
                ('agent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.Agent')),
                ('marbete_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dgii.Marbete')),
            ],
            options={
                'ordering': ['-created'],
                'db_table': 'detection',
            },
        ),
    ]