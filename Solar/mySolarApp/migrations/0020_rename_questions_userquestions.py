# Generated by Django 4.0.5 on 2022-07-14 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0019_rename_help_questions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='questions',
            new_name='userQuestions',
        ),
    ]
