from django.db import models
from django.utils.html import mark_safe
from .Category import Category
from .Breed import Breed
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


def validate_svg_file(value):
    FileExtensionValidator(
        allowed_extensions=['svg'],
        message=_('%(value)s файл должен быть векторным .svg изображением')
    )(value)


class Service(models.Model):
    CAT = 'cat'
    DOG = 'dog'
    ANY = 'any'

    animals = {
        CAT: 'Кошка',
        DOG: 'Собака',
        ANY: 'Любая',
    }

    BREEDS = [
        (CAT, 'Кошка'),
        (DOG, 'Собака'),
        (ANY, 'Любая'),
    ]

    title = models.CharField(max_length=30, verbose_name='Название услуги')
    text = models.TextField(verbose_name='Описание', blank=True, default='')
    animal = models.CharField(
        max_length=3, choices=BREEDS, default=ANY, verbose_name='Вид животного')
    price = models.CharField(max_length=20, default='0', verbose_name='Цена')
    time = models.CharField(max_length=20, default='',
                            verbose_name='Продолжительность', blank=True)
    img = models.FileField(
        upload_to='services',
        verbose_name='Картинка',
        null=True,
        blank=True,
        validators=[validate_svg_file]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='Порода'
    )

    # def img_tag(self):
    #     return u'<img src="%s" />' % mark_safe(f'<img src="/services/{self.img}" width="150" height="150" />')

    # img_tag.short_description = 'Image'
    # img_tag.allow_tags = True

    def __str__(self):
        return f'{self.title} - {self.animals[self.animal]} - {self.category}'

    class Meta:
        verbose_name = 'Услугу'
        verbose_name_plural = 'Услуги'
