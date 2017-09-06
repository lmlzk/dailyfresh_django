# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('goods_type_id', models.SmallIntegerField(choices=[(1, '新鲜水果'), (2, '海鲜水产'), (3, '猪牛羊肉'), (4, '禽类蛋品'), (5, '新鲜蔬菜'), (6, '速冻食品')], default=1, verbose_name='商品类型id')),
                ('goods_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('goods_desc', models.CharField(max_length=256, verbose_name='商品描述')),
                ('goods_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')),
                ('transit_price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品运费')),
                ('goods_unite', models.CharField(max_length=20, verbose_name='商品单位')),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品详情')),
                ('goods_stock', models.IntegerField(default=0, verbose_name='商品库存')),
                ('goods_sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('goods_status', models.SmallIntegerField(default=1, verbose_name='商品状态')),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品描述')),
            ],
            options={
                'verbose_name': 'de商品信息',
                'verbose_name_plural': 'de商品信息',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('img_url', models.ImageField(upload_to='/images/goods/', verbose_name='图片路径')),
                ('is_def', models.BooleanField(verbose_name='是否默认', default=False)),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='所属商品')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
