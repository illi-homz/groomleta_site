from tkinter import CASCADE
from django.db import models
from .Service import Service


class OrderService(models.Model):
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.DO_NOTHING)
    count = models.SmallIntegerField(verbose_name='Количество', default=0, blank=True)

    def __str__(self):
        return f'{self.service.title} ({self.count})'
	
    class Meta:
        verbose_name = 'Услуга заказа'
        verbose_name_plural = 'Услуги заказов'
