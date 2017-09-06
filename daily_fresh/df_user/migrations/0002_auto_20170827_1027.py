# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passport',
            name='email',
            field=models.EmailField(unique=True, verbose_name='邮箱', max_length=254),
        ),
        migrations.AlterField(
            model_name='passport',
            name='username',
            field=models.CharField(unique=True, verbose_name='用户名', max_length=20),
        ),
    ]
