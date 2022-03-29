from django.db import models

help_text = '!!!Тезисы разделять точкой с запятой ";". Это важно. Иначе будет один сплошной текст.'

class Question(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    punkts = models.TextField(help_text=help_text, verbose_name='Тезисы')
	
    def __str__(self):
        return self.title
