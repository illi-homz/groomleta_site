from django.db import models
from django.utils.timezone import now
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files import File

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название товара')
    vendor_code = models.CharField(max_length=30, verbose_name='Артикул', blank=True, default='')
    count = models.SmallIntegerField(verbose_name='Количество', blank=True, default=0)
    price = models.IntegerField(verbose_name='Цена', blank=True, default=0)
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    img = models.FileField(upload_to='products', verbose_name='Картинка', blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='Дата регистрации', default=now)
    update_date = models.DateTimeField(verbose_name='Дата обновления', default=now)

    def __str__(self):
        return f'{self.vendor_code} - {self.title}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        def save_img():
            target_witch = 640
        
            image = Image.open(self.img)
            image = image.convert('RGB')  # Convert Image to RGB color mode
            (w, h) = image.size or ()
            coff = target_witch / int(w)
            image = image.resize((target_witch, int(float(h) * coff)))
            image = ImageOps.exif_transpose(image) # auto_rotate image according to EXIF data
            im_io = BytesIO()  # save image to BytesIO object
            image.save(im_io, 'JPEG', quality=70) # save image to BytesIO object
            new_image = File(im_io, name='product.jpg') # create a django-friendly Files object
            self.img = new_image # Change to new image
        
        if (self.img):
            save_img()
            
        super().save(*args, **kwargs)
