# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Katale', '0009_auto_20151014_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(related_name='subcategories', to='Katale.Category', null=True),
        ),
        migrations.AlterModelTable(
            name='subcategory',
            table='subcategories',
        ),
    ]
