# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-13 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='name',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
