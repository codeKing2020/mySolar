# Generated by Django 4.0.5 on 2022-08-12 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0030_alter_delivery_info_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]