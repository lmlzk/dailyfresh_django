# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0004_auto_20170829_1221'),
        ('df_goods', '0003_delete_goodsinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrowseHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='所属商品')),
                ('passport', models.ForeignKey(to='df_user.Passport', verbose_name='所属用户')),
            ],
            options={
                'db_table': 's_browse_history',
            },
        ),
    ]
