# Generated by Django 4.0.4 on 2022-06-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0007_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_shopkeeper',
            field=models.BooleanField(default=False),
        ),
    ]