from datetime import datetime
from django.db import models


class Callback(models.Model):
    name = models.CharField(max_length=50, verbose_name='Клиент')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_completed = models.BooleanField(verbose_name='Обработан', default=False)
	
    def __str__(self):
        # date = datetime
        return f'{self.create_date.strftime("%H:%M %d-%m-%Y")} {self.name}'

    class Meta:
        verbose_name = 'Заказ звонка'
        verbose_name_plural = 'Заказ звонка'
