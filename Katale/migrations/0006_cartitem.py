# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Katale', '0005_auto_20150818_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cart_id', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(to='Katale.Product')),
            ],
            options={
                'ordering': ['date_added'],
                'db_table': 'Cart_Items',
            },
        ),
    ]
