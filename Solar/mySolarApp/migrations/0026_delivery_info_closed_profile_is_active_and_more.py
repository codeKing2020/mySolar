# Generated by Django 4.0.5 on 2022-07-30 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0025_delivery_info_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_info',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='shopkeeper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
