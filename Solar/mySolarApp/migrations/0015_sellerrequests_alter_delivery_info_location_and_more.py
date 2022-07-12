# Generated by Django 4.0.5 on 2022-07-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0014_rename_how_activewillyoubeperweek_profile_how_active_and_more'),
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
            ],
        ),
        migrations.AlterField(
            model_name='delivery_info',
            name='location',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=128),
        ),
    ]