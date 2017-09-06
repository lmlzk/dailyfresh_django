# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.FloatField(default=0, verbose_name='小计'),
        ),
    ]
