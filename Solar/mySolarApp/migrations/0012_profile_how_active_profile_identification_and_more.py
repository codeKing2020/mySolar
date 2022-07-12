# Generated by Django 4.0.5 on 2022-07-10 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0011_alter_delivery_info_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='how_active',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='identification',
            field=models.CharField(default='null', max_length=13),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(default='null', max_length=86),
            preserve_default=False,
        ),
    ]