# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-09 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_mainshow'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gnum', models.IntegerField(default=0)),
                ('select', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('typeid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('typename', models.CharField(max_length=20)),
                ('childtypenames', models.CharField(max_length=200)),
                ('typesort', models.IntegerField(default=1024)),
            ],
            options={
                'db_table': 'axf_foodtypes',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.CharField(max_length=20)),
                ('productimg', models.CharField(max_length=200)),
                ('productname', models.CharField(max_length=100)),
                ('productlongname', models.CharField(max_length=100, verbose_name='商品名称')),
                ('isxf', models.BooleanField(default=False, verbose_name='是否精选')),
                ('pmdesc', models.BooleanField(default=False, verbose_name='店长推荐')),
                ('specifics', models.CharField(max_length=20, verbose_name='规格')),
                ('price', models.FloatField(default=0, verbose_name='价格')),
                ('marketprice', models.FloatField(default=0, verbose_name='市场价')),
                ('childcid', models.IntegerField(blank=True, default=None, null=True)),
                ('childcidname', models.CharField(max_length=20, verbose_name='小类')),
                ('dealerid', models.CharField(max_length=20, verbose_name='商家id')),
                ('storenums', models.IntegerField(default=0, verbose_name='库存')),
                ('productnum', models.IntegerField(default=0, verbose_name='销量')),
                ('onSale', models.BooleanField(default=True)),
                ('categoryid', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.FoodType', verbose_name='大类')),
            ],
            options={
                'verbose_name_plural': '商品',
                'db_table': 'axf_goods',
            },
            managers=[
                ('gmanager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otime', models.DateTimeField(auto_now_add=True)),
                ('ostatus', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20, unique=True)),
                ('upwd', models.CharField(max_length=20)),
                ('uicon', models.ImageField(upload_to='')),
                ('utoken', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('ulevel', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_user',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='ouser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.User'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Goods'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.Order'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.User'),
        ),
    ]
