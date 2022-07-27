# Generated by Django 4.0.5 on 2022-07-27 15:17

from django.conf import settings
from django.db import migrations, models
import mySolarApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0026_delivery_info_closed_profile_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='shopkeeper',
            field=models.ForeignKey(on_delete=models.SET(mySolarApp.models.Profile.deactivate_shopkeeper), related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
