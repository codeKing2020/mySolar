# Generated by Django 4.0.5 on 2022-07-10 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0013_rename_desc_profile_bio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='how_activeWillYouBePerWeek',
            new_name='how_active',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='identificationNumber',
            new_name='identification',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='nameOfCompany',
            new_name='name',
        ),
    ]
