# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-13 16:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ost-reservation', '0006_auto_20170513_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='last_res_made',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 13, 16, 46, 8, 208951, tzinfo=utc), verbose_name='Last made reservation on resource'),
            preserve_default=False,
        ),
    ]