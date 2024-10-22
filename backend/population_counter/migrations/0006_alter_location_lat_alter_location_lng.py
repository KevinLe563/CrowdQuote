# Generated by Django 4.2.3 on 2023-07-23 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('population_counter', '0005_rename_latitude_location_lat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='location',
            name='lng',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
    ]
