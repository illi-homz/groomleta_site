from django.utils.timezone import now
from django.db import models
from django.utils.html import mark_safe
from .Service import Service
from .Master import Master
from .Client import Client


class Event(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название записи')
    start_date = models.DateTimeField(verbose_name='Дата и время записи', default=now)
    end_date = models.DateTimeField(verbose_name='Дата и время окончания', default=now)
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        verbose_name='Клиент',
        blank=True,
        null=True,
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.DO_NOTHING,
        verbose_name='Мастер',
        blank=True,
        null=True,
    )
    comment = models.TextField(verbose_name='Комментарий', default='')
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def get_services(self):
        return ", ".join([f'{s.title} ({s.breed})' for s in self.services.all()])
