# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-09 02:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mainshow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=20)),
                ('trackid', models.CharField(max_length=20)),
                ('categoryid', models.CharField(max_length=20)),
                ('brandname', models.CharField(max_length=20)),
                ('img1', models.CharField(max_length=200)),
                ('childcid1', models.CharField(max_length=20)),
                ('productid1', models.CharField(max_length=20)),
                ('longname1', models.CharField(max_length=100)),
                ('price1', models.FloatField(default=0)),
                ('marketprice1', models.FloatField(default=0)),
                ('img2', models.CharField(max_length=200)),
                ('childcid2', models.CharField(max_length=20)),
                ('productid2', models.CharField(max_length=20)),
                ('longname2', models.CharField(max_length=100)),
                ('price2', models.FloatField(default=0)),
                ('marketprice2', models.FloatField(default=0)),
                ('img3', models.CharField(max_length=200)),
                ('childcid3', models.CharField(max_length=20)),
                ('productid3', models.CharField(max_length=20)),
                ('longname3', models.CharField(max_length=100)),
                ('price3', models.FloatField(default=0)),
                ('marketprice3', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'axf_mainshow',
            },
        ),
    ]
