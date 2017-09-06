# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='creat_time',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='creat_time',
            new_name='create_time',
        ),
    ]
