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
    
    username = models.CharField(max_length=50, verbose_name='Имя', blank=False)
    lastname = models.CharField(max_length=50, verbose_name='Фамилия', blank=False)
    avatar = models.ImageField(upload_to='masters', verbose_name='Фотка', default='', blank=True)
    education = models.CharField(max_length=100, verbose_name='Образование', default='Без образования')
    phone = models.CharField(max_length=20, verbose_name='Телефон', default='', blank=True)
    post = models.CharField(max_length=20, verbose_name='Должность', choices=POSTS, default=GROOMMER)
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)
	
    def __str__(self):
        return f'{self.username} {self.lastname}'

    class Meta:
        verbose_name = 'Грумер'
        verbose_name_plural = 'Грумеры'
