# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20170829_1221'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GoodsInfo',
        ),
    ]
