# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-22 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MusicInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='音乐名')),
                ('download_count', models.IntegerField(default=0, verbose_name='下载量')),
                ('star_one', models.IntegerField(default=0, verbose_name='一星数')),
                ('star_two', models.IntegerField(default=0, verbose_name='二星数')),
                ('star_three', models.IntegerField(default=0, verbose_name='三星数')),
                ('star_four', models.IntegerField(default=0, verbose_name='四星数')),
                ('star_five', models.IntegerField(default=0, verbose_name='五星数')),
                ('star_avg', models.FloatField(default=0, verbose_name='平均星数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('url', models.CharField(max_length=1000, verbose_name='音乐资源链接')),
            ],
            options={
                'db_table': 'music_information',
            },
        ),
        migrations.CreateModel(
            name='MusicKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_word', models.CharField(max_length=50, unique=True, verbose_name='关键字')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('musicinformation', models.ManyToManyField(to='music.MusicInformation')),
            ],
            options={
                'db_table': 'music_keyword',
            },
        ),
    ]
