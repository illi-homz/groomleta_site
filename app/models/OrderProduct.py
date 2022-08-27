from tkinter import CASCADE
from django.db import models
from .Product import Product


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.DO_NOTHING)
    count = models.SmallIntegerField(verbose_name='Количество', default=0, blank=True)
	
    def __str__(self):
        return f'{self.product.title} ({self.count})'
    
    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'
