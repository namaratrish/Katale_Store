# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Katale', '0007_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='category_name',
            field=models.ForeignKey(to='Katale.Category', null=True),
        ),
    ]
