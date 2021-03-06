# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-08 00:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ost-reservation', '0002_auto_20170507_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='resource',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='OSTUser',
        ),
    ]
