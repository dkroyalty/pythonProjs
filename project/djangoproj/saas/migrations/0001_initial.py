# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
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
    ]
