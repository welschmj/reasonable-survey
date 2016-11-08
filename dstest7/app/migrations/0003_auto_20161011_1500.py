# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_question_desc_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='next_qid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_branch', to='app.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='next_qid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Question'),
        ),
    ]