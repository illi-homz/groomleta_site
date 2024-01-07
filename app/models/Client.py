from django.db import models
from django.utils.timezone import now

class ClientManager(models.Manager):
    def get_queryset(self):
        return super(ClientManager, self).get_queryset().filter(is_active=True)


class Client(models.Model):
    username = models.CharField(max_length=50, verbose_name='Имя')
    lastname = models.CharField(max_length=50, verbose_name='Фамилия', blank=True)
    avatar = models.ImageField(upload_to='masters', verbose_name='Фотка', default='', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', default='', blank=True)
    comment = models.TextField(verbose_name='Заметки', default='', blank=True)
    animal = models.CharField(max_length=100, verbose_name='Животное', default='', blank=True)
    address = models.CharField(max_length=200, verbose_name='Адрес', default='', blank=True)
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)
    update_date = models.DateTimeField(verbose_name='Дата обновления', default=now)
    is_blocked = models.BooleanField(verbose_name='Заблокирован', default=False, blank=True)
    is_active = models.BooleanField(default=True)

    objects = ClientManager()

	
    def __str__(self):
        return f'{self.username} {self.lastname}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
