# Generated by Django 4.0.3 on 2024-03-05 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_smsnotification_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsnotification',
            name='error_message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='smsnotification',
            name='success',
            field=models.BooleanField(default=True),
        ),
    ]
