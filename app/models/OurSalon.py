from django.db import models


class OurSalon(models.Model):
    title = models.CharField(max_length=50, default='')
    img = models.ImageField(upload_to='outworks', verbose_name='Фото')
	
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фото салона'
        verbose_name_plural = 'Фоты салона'
