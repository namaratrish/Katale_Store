# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Katale', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('image', models.ImageField(max_length=50, upload_to=b'images')),
            ],
            options={
                'db_table': 'Products',
            },
        ),
    ]
