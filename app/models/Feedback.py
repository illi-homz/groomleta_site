from email.policy import default
from django.db import models


class Feedback(models.Model):
    nick = models.CharField(max_length=30, verbose_name='Ник')
    avatar = models.ImageField(upload_to='feedbacks', verbose_name='Аватарка', default='', blank=True)
    text = models.TextField(verbose_name='Текст отзыва')
	
    def __str__(self):
        return self.nick
