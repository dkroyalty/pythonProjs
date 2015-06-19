# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Websites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('webseq', models.IntegerField(default=0)),
                ('website', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255)),
                ('detail', models.TextField()),
            ],
            options={
                'ordering': ['webseq', 'desc'],
            },
        ),
    ]
