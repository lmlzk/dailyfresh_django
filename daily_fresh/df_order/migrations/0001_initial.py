# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0004_auto_20170829_1221'),
        ('df_goods', '0004_browsehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBasic',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('order_id', models.CharField(primary_key=True, serialize=False, verbose_name='订单id', max_length=64)),
                ('total_count', models.IntegerField(default=1, verbose_name='商品总数')),
                ('total_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总额')),
                ('transit_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单运费')),
                ('pay_method', models.IntegerField(default=1, verbose_name='支付方式')),
                ('order_status', models.IntegerField(default=1, verbose_name='订单状态')),
                ('addr', models.ForeignKey(to='df_user.Address', verbose_name='收件地址')),
                ('passport', models.ForeignKey(to='df_user.Passport', verbose_name='用户')),
            ],
            options={
                'db_table': 's_order_basic',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('goods_count', models.IntegerField(default=1, verbose_name='商品数目')),
                ('goods_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='商品')),
                ('order', models.ForeignKey(to='df_order.OrderBasic', verbose_name='基本订单')),
            ],
            options={
                'db_table': 's_order_detail',
            },
        ),
    ]
