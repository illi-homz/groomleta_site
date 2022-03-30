from django.db import models


class Promo(models.Model):
    title = models.CharField(max_length=50, default='')
    mobile_img = models.ImageField(upload_to='promo', verbose_name='Баннер для моб устройств')
    tablet_img = models.ImageField(upload_to='promo', verbose_name='Баннер для компа')
	
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Акции'
        verbose_name_plural = 'Акции'
