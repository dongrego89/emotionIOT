# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-05-25 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appQRMusical', '0008_auto_20190525_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta_quizz',
            name='multimediaPregunta',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='pregunta+', to='appQRMusical.Multimedia'),
        ),
    ]
