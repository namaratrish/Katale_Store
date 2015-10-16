# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Katale', '0008_auto_20151014_0944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='category_name',
            new_name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(related_name='child', blank=True, to='Katale.Category', null=True),
        ),
    ]
