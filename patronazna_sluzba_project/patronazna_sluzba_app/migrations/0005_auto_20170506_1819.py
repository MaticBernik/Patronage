# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-06 16:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0004_auto_20170506_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 7, 18, 19, 21, 849293)),
        ),
    ]
