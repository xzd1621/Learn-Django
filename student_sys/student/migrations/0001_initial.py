# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='姓名', max_length=128)),
                ('sex', models.IntegerField(verbose_name='性别', choices=[(3, '未知'), (2, '女'), (1, '男')])),
                ('profession', models.CharField(verbose_name='职业', max_length=128)),
                ('email', models.EmailField(verbose_name='Email', max_length=254)),
                ('qq', models.CharField(verbose_name='QQ', max_length=128)),
                ('phone', models.CharField(verbose_name='电话', max_length=128)),
                ('status', models.IntegerField(verbose_name='审核状态', default=0, choices=[(3, '未知'), (2, '女'), (1, '男')])),
                ('created_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
            ],
            options={
                'verbose_name': '学员信息',
                'verbose_name_plural': '学员信息',
            },
        ),
    ]
