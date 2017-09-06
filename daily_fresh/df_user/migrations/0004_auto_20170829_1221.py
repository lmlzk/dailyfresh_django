# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0003_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='creat_time',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='passport',
            old_name='creat_time',
            new_name='create_time',
        ),
    ]
