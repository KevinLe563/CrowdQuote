# Generated by Django 4.2.3 on 2023-07-23 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('population_counter', '0004_location_latitude_location_longitude'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='latitude',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='longitude',
            new_name='lng',
        ),
    ]
