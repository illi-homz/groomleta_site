# Generated by Django 4.0.3 on 2024-04-07 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_smsnotification_error_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_notificate',
            field=models.BooleanField(default=True, verbose_name='Уведомлять?'),
        ),
    ]
