# Generated by Django 4.0.5 on 2022-07-23 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0024_delivery_info_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_info',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='seller_deliveryInfo', to='mySolarApp.profile'),
            preserve_default=False,
        ),
    ]
