from django.db import models
from django.utils.timezone import now


class Client(models.Model):
    username = models.CharField(max_length=50, verbose_name='Имя', blank=False)
    lastname = models.CharField(max_length=50, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='masters', verbose_name='Фотка', default='', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', default='', blank=True)
    comment = models.TextField(verbose_name='Заметки', default='')
    address = models.TextField(verbose_name='Адресс', default='')
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)
	
    def __str__(self):
        return f'{self.username} {self.lastname}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
