# Generated by Django 4.0.3 on 2022-11-11 20:54

import app.models.Service
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_orderservice_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='services', verbose_name='Картинка'),
        ),
    ]
