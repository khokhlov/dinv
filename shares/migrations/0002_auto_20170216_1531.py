# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 12:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shareitem',
            old_name='portfolie',
            new_name='portfolio',
        ),
    ]