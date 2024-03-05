from django.db import models
from django.utils.timezone import now
from .Client import Client


class SmsNotification(models.Model):
    created = models.DateTimeField(default=now)
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    error_message = models.TextField(default='')
    success = models.BooleanField(default=True)
