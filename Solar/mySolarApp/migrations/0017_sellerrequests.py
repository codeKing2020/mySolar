# Generated by Django 4.0.5 on 2022-07-12 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0016_delete_sellerrequests'),
    ]

    operations = [
        migrations.CreateModel(
            name='sellerRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellerFName', models.CharField(max_length=24)),
                ('sellerLName', models.CharField(max_length=24)),
                ('businessEmail', models.EmailField(max_length=254)),
                ('businessContact', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('location', models.CharField(max_length=128)),
                ('bio', models.CharField(max_length=1000)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_and_banner_images')),
                ('banner_pic', models.ImageField(blank=True, upload_to='profile_and_banner_images')),
                ('how_active', models.IntegerField()),
                ('identification', models.CharField(max_length=13, unique=True)),
                ('sellerAcc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
