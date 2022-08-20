from django.utils.timezone import now
from django.db import models
from .Service import Service
from .Master import Master
from .Client import Client


class Event(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название записи')
    start_date = models.DateTimeField(verbose_name='Дата и время записи', default=now)
    end_date = models.DateTimeField(verbose_name='Дата и время окончания', default=now)
    services = models.ManyToManyField(Service, verbose_name='Услуги', blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        verbose_name='Клиент',
        blank=True,
        null=True,
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        verbose_name='Мастер',
        blank=True,
        null=True,
        default=None
    )
    comment = models.TextField(verbose_name='Комментарий', default='', blank=True)
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)
    update_date = models.DateTimeField(verbose_name='Дата обновления', default=now)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def get_services(self):
        return ", ".join([f'{s.title} ({s.breed})' for s in self.services.all()])
