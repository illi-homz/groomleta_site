# Generated by Django 4.0.3 on 2024-04-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_delete_smsnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_notificate',
        ),
        migrations.AddField(
            model_name='service',
            name='is_notificate',
            field=models.BooleanField(default=True, verbose_name='Уведомлять?'),
        ),
    ]