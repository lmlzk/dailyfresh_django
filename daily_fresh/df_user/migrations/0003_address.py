# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20170827_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('recipicent_name', models.CharField(verbose_name='收件人', max_length=20)),
                ('recipicent_addr', models.CharField(verbose_name='收件地址', max_length=256)),
                ('zip_code', models.CharField(verbose_name='邮编', max_length=6)),
                ('recipicent_phone', models.CharField(verbose_name='联系电话', max_length=11)),
                ('is_def', models.BooleanField(default=False, verbose_name='是否默认')),
                ('passport', models.ForeignKey(to='df_user.Passport', verbose_name='所属账户')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
    ]
