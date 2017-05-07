# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-07 21:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='res start')),
                ('end_time', models.DateTimeField(verbose_name='res end')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField(verbose_name='available from')),
                ('end_time', models.DateTimeField(verbose_name='available until')),
                ('tags', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('pw', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='resource',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ost-reservation.User'),
        ),
        migrations.AddField(
            model_name='reservations',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ost-reservation.User'),
        ),
        migrations.AddField(
            model_name='reservations',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ost-reservation.Resource'),
        ),
    ]
