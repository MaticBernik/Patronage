# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-08 15:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0006_auto_20170607_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material_Obisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolicina', models.IntegerField(default=1)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Material')),
                ('obisk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Obisk')),
            ],
        ),
        migrations.CreateModel(
            name='Zdravilo_Obisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolicina', models.IntegerField(default=1)),
                ('obisk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Obisk')),
                ('zdravilo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Zdravilo')),
            ],
        ),
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_konec',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 9, 15, 59, 26, 799587)),
        ),
        migrations.AlterField(
            model_name='plan',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 9, 15, 59, 26, 797867)),
        ),
    ]
