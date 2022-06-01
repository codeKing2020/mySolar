# Generated by Django 4.0.4 on 2022-06-01 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mySolarApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='store_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.CharField(max_length=1000, verbose_name='Link to picture')),
                ('short_desc', models.CharField(max_length=150, verbose_name='Short Description')),
                ('long_desc', models.CharField(max_length=5000, verbose_name='Long Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
