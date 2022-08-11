from django.db import models
from django.utils.html import mark_safe
# from .Breed import Breed
from django.utils.timezone import now


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название товара')
    vendor_code = models.CharField(max_length=30, verbose_name='Артикул', blank=True, default='')
    count = models.SmallIntegerField(verbose_name='Количество', blank=True, default=0)
    price = models.IntegerField(verbose_name='Цена', blank=True, default=0)
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    img = models.FileField(upload_to='services', verbose_name='Картинка', blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)
    update_date = models.DateTimeField(verbose_name='Дата обновления', default=now)

    def __str__(self):
        return f'{self.vendor_code} - {self.title}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
