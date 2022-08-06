from django.contrib import admin
from django.utils.html import format_html
from . import models


def dublicate_ad(modeladmin, request, queryset):
    # клонирование выбранных Ad
    for el in queryset:
        el.pk = None
        el.save()


dublicate_ad.short_description = "Дублировать объект"


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'img', 'image_tag')
    list_editable = ['img']
    actions = [dublicate_ad]

    def image_tag(self, obj):
        return format_html('<img width="100" src="{}" />'.format(obj.img.url))

    image_tag.short_description = 'Картинка'


@admin.register(models.OurWork)
class OurWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img')
    list_editable = ['title', 'img']
    actions = [dublicate_ad]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'punkts')
    list_editable = ['title', 'punkts']
    actions = [dublicate_ad]


@admin.register(models.Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'mobile_img', 'tablet_img')
    list_editable = ['title', 'mobile_img', 'tablet_img']
    actions = [dublicate_ad]
    list_per_page = 10

@admin.register(models.Сategory)
class СategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_editable = ['title']
    actions = [dublicate_ad]

@admin.register(models.Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_editable = ['title']
    actions = [dublicate_ad]

@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'animal', 'price', 'image_tag')
    list_editable = ['title', 'category', 'animal', 'price']
    list_filter = ['title', 'animal', 'category']
    search_fields = ['title']
    actions = [dublicate_ad]
    list_per_page = 10
    ordering = ('id',)

    def image_tag(self, obj):
        return format_html('<img width="50" src="{}" />'.format(obj.img.url))

    image_tag.short_description = 'Картинка'

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'nick', 'is_approved')
    list_editable = ['is_approved']
    search_fields = ['name', 'phone']
    readonly_fields = [
        'nick',
        'avatar',
        'text',
        'create_date',
    ]
    list_per_page = 10
    ordering = ('id',)

@admin.register(models.Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'name', 'phone', 'is_completed')
    list_editable = ['is_completed']
    list_filter = ['name', 'phone']
    search_fields = ['name', 'phone']
    readonly_fields = [
        'name',
        'phone',
        'create_date',
    ]
    actions = [dublicate_ad]
    list_per_page = 10
    ordering = ('id',)


@admin.register(models.ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'current_date', 'name', 'phone',
                    'services', 'min_price', 'is_processed')
    list_editable = ['is_processed']
    list_filter = ['name', 'phone', 'current_date']
    search_fields = ['name', 'phone']
    readonly_fields = [
        'name',
        'phone',
        'min_price',
        'create_date',
    ]
    actions = [dublicate_ad]
    list_per_page = 10
    ordering = ('id',)
