from django.db import models
# from datetime import datetime
from django.utils.timezone import now


class Service(models.Model):
    name = models.CharField(max_length=30, verbose_name='Ник')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    min_price = models.SmallIntegerField(verbose_name='Мин цена')
    services = models.TextField(verbose_name='Услуги')
    comment = models.TextField(verbose_name='Комментарий', blank=True, default='')
    current_date = models.DateField(verbose_name='Дата записи')
    create_date = models.DateTimeField(verbose_name='Дата создания', default=now)
    is_processed = models.BooleanField(verbose_name='Обработан', default=False)
	
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Запись на прием'
