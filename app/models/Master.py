from django.db import models
from django.utils.timezone import now
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files import File


class MasterManager(models.Manager):
    def get_all(self):
        return super(MasterManager, self).get_queryset().all()
    
    def get_queryset(self):
        return super(MasterManager, self).get_queryset().filter(is_active=True)

class Master(models.Model):
    MAIN_GROOMMER = 'main_groommer'
    GROOMMER = 'groommer'
    HELPER = 'helper'

    POSTS = [
        (MAIN_GROOMMER, 'Главный груммер'),
        (GROOMMER, 'Груммер'),
        (HELPER, 'Помощник груммера'),
    ]

    username = models.CharField(max_length=50, verbose_name='Имя')
    lastname = models.CharField(
        max_length=50, verbose_name='Фамилия', default='', blank=True)
    avatar = models.ImageField(
        upload_to='masters', verbose_name='Фотка', default='', blank=True)
    education = models.CharField(
        max_length=100, verbose_name='Образование', default='Без образования', blank=True)
    phone = models.CharField(
        max_length=20, verbose_name='Телефон', default='', blank=True)
    post = models.CharField(
        max_length=20, verbose_name='Должность', choices=POSTS, default=GROOMMER)
    color = models.CharField(
        max_length=10, verbose_name='Цвет', default='#FFC11C')
    comment = models.TextField(verbose_name='Заметки', default='', blank=True)
    rate = models.SmallIntegerField(
        verbose_name='Ставка', default=0, blank=True)
    address = models.CharField(
        max_length=50, verbose_name='Адрес', default='', blank=True)
    create_date = models.DateTimeField(
        verbose_name='Дата регистрации', default=now)
    update_date = models.DateTimeField(
        verbose_name='Дата обновления', default=now)
    is_active = models.BooleanField(default=True)

    objects = MasterManager()


    def __str__(self):
        return f'{self.username} {self.lastname}'

    class Meta:
        verbose_name = 'Грумер'
        verbose_name_plural = 'Грумеры'

    def save(self, *args, **kwargs):
        def save_img():
            target_witch = 640
        
            image = Image.open(self.avatar)
            image = image.convert('RGB')  # Convert Image to RGB color mode
            (w, h) = image.size or ()
            coff = target_witch / int(w)
            image = image.resize((target_witch, int(float(h) * coff)))
            image = ImageOps.exif_transpose(image) # auto_rotate image according to EXIF data
            im_io = BytesIO()  # save image to BytesIO object
            image.save(im_io, 'JPEG', quality=70) # save image to BytesIO object
            new_image = File(im_io, name='groomer.jpg') # create a django-friendly Files object
            self.avatar = new_image # Change to new image
        
        if (self.avatar):
            save_img()
            
        super().save(*args, **kwargs)
