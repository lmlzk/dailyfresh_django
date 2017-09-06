# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0004_browsehistory'),
        ('df_user', '0004_auto_20170829_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('goods_count', models.IntegerField(verbose_name='商品数目', default=1)),
                ('goods', models.ForeignKey(verbose_name='商品', to='df_goods.Goods')),
                ('passport', models.ForeignKey(verbose_name='用户', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_cart',
            },
        ),
    ]
