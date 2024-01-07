from django.db import models
from django.utils.timezone import now
from .Master import Master
from .Client import Client
from .OrderProduct import OrderProduct
from .OrderService import OrderService

class OrderManager(models.Manager):
    def get_queryset(self):
        return super(OrderManager, self).get_queryset().filter(is_active=True)


class Order(models.Model):
    price = models.SmallIntegerField(verbose_name='Цена', default=0, blank=True)
    products = models.ManyToManyField(OrderProduct, verbose_name='Продукты', blank=True)
    services = models.ManyToManyField(OrderService, verbose_name='Услуги', blank=True)
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
    )
    is_success = models.BooleanField(verbose_name='Оплачен', default=False, blank=True)
    is_cancel = models.BooleanField(verbose_name='Отменен', default=False, blank=True)
    is_reserved = models.BooleanField(verbose_name='Забронирован', default=False, blank=True)
    update_date = models.DateTimeField(verbose_name='Дата обновления', default=now)
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)
    is_active = models.BooleanField(default=True)

    objects = OrderManager()

	
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
