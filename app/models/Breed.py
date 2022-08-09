from django.db import models

class Breed(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название породы')
	
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Породу'
        verbose_name_plural = 'Породы'
