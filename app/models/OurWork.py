from django.db import models


class OurWork(models.Model):
    title = models.CharField(max_length=50, default='')
    img = models.ImageField(upload_to='outworks', verbose_name='Наши работы')
	
    def __str__(self):
        return self.title
