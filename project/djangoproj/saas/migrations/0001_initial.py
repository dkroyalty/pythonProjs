# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemname', models.CharField(max_length=255, db_index=True)),
                ('itemimg', models.CharField(default=b'', max_length=255)),
                ('itemdesc', models.TextField(default=b'', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placename', models.CharField(max_length=255, db_index=True)),
                ('placeimg', models.CharField(default=b'', max_length=255)),
                ('imgrect', models.CharField(default=b'', max_length=255)),
                ('placedesc', models.TextField(default=b'', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceHoldItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createdata', models.DateTimeField(default=datetime.datetime.now)),
                ('itemdata', models.ForeignKey(to='saas.ItemData')),
                ('placedata', models.ForeignKey(to='saas.PlaceData')),
            ],
            options={
                'ordering': ['createdata'],
            },
        ),
        migrations.CreateModel(
            name='PlaceRelations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parentplace', models.ForeignKey(related_name='parent_id', to='saas.PlaceData')),
                ('sonplace', models.ForeignKey(related_name='son_id', to='saas.PlaceData')),
            ],
        ),
        migrations.CreateModel(
            name='StatusMaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=255, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaxStandard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taxbyself', models.IntegerField(default=0)),
                ('taxbyother', models.IntegerField(default=0)),
                ('taxrate', models.IntegerField(default=0, db_index=True)),
                ('taxfastsub', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['taxrate'],
            },
        ),
        migrations.CreateModel(
            name='TypeMaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typename', models.CharField(max_length=255, db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='itemdata',
            name='itemstatus',
            field=models.ForeignKey(to='saas.StatusMaster'),
        ),
        migrations.AddField(
            model_name='itemdata',
            name='itemtype',
            field=models.ForeignKey(to='saas.TypeMaster'),
        ),
    ]
