# Generated by Django 4.2.3 on 2023-07-22 17:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('population_counter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
        migrations.AddField(
            model_name='location',
            name='civic_number',
            field=models.PositiveIntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='postal_code',
            field=models.CharField(default='N2L 0K4', max_length=6, validators=[django.core.validators.RegexValidator('[A-Z]\\d[A-Z]\\s\\d[A-Z]\\d')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='street_name',
            field=models.CharField(default='University Ave', max_length=100),
            preserve_default=False,
        ),
    ]
