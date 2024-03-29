from django.db import models

help_text = '!!!Каждый тезис писать на новой строке. Это важно. Иначе будет один сплошной текст.'

class Question(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    punkts = models.TextField(help_text=help_text, verbose_name='Тезисы')
	
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос и ответ'
        verbose_name_plural = 'Вопросы и ответы'
