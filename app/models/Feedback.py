from django.db import models
# from datetime import datetime
from django.utils.timezone import now


class Feedback(models.Model):
    nick = models.CharField(max_length=30, verbose_name='Ник')
    avatar = models.ImageField(upload_to='feedbacks', verbose_name='Аватарка', default='', blank=True)
    text = models.TextField(verbose_name='Текст отзыва')
    create_date = models.DateTimeField(verbose_name='Дата создания', default=now)
    is_approved = models.BooleanField(verbose_name='Подтвержен', default=False)
	
    def __str__(self):
        return self.nick

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
