# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('continent', models.CharField(max_length=4)),
                ('capital', models.CharField(max_length=255)),
                ('geoname_id', models.IntegerField()),
                ('languages', models.CharField(max_length=255)),
                ('north', models.FloatField()),
                ('south', models.FloatField()),
                ('iso_alpha_3', models.CharField(max_length=3)),
                ('fips_code', models.CharField(max_length=3)),
                ('population', models.CharField(max_length=255)),
                ('east', models.FloatField()),
                ('iso_numeric', models.CharField(max_length=255)),
                ('area_in_sq_km', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=2)),
                ('west', models.FloatField()),
                ('country_name', models.CharField(max_length=255)),
                ('continent_name', models.CharField(max_length=255)),
                ('currency_code', models.CharField(max_length=4)),
            ],
        ),
    ]