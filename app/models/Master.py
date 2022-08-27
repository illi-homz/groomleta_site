from django.db import models
from django.utils.timezone import now


class Master(models.Model):
    MAIN_GROOMMER = 'main_groommer'
    GROOMMER = 'groommer'
    HELPER = 'helper'

    POSTS = [
        (MAIN_GROOMMER, 'Главный груммер'),
        (GROOMMER, 'Груммер'),
        (HELPER, 'Помощник груммера'),
    ]
    
    username = models.CharField(max_length=50, verbose_name='Имя')
    lastname = models.CharField(max_length=50, verbose_name='Фамилия', default='', blank=True)
    avatar = models.ImageField(upload_to='masters', verbose_name='Фотка', default='', blank=True)
    education = models.CharField(max_length=100, verbose_name='Образование', default='Без образования', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', default='', blank=True)
    post = models.CharField(max_length=20, verbose_name='Должность', choices=POSTS, default=GROOMMER)
    color = models.CharField(max_length=10, verbose_name='Цвет', default='#FFC11C')
    comment = models.TextField(verbose_name='Заметки', default='', blank=True)
    rate = models.SmallIntegerField(verbose_name='Ставка', default=0, blank=True)
    address = models.CharField(max_length=50, verbose_name='Адрес', default='', blank=True)
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)
    update_date = models.DateTimeField(verbose_name='Дата обновления', default=now)
	
    def __str__(self):
        return f'{self.username} {self.lastname}'

    class Meta:
        verbose_name = 'Грумер'
        verbose_name_plural = 'Грумеры'
