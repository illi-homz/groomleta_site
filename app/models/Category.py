from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
	
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
