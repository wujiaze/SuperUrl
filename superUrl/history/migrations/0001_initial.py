# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-24 20:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=20, verbose_name='查询关键字')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
            ],
            options={
                'db_table': 'history',
            },
        ),
    ]