from django.contrib import admin
from . import models


def dublicate_ad(modeladmin, request, queryset):
    # клонирование выбранных Ad
    for el in queryset:
        el.pk = None
        el.save()


dublicate_ad.short_description = "Дублировать объект"


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    actions = [dublicate_ad]


@admin.register(models.OurWork)
class OurWorkAdmin(admin.ModelAdmin):
    actions = [dublicate_ad]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    actions = [dublicate_ad]


@admin.register(models.Promo)
class PromoAdmin(admin.ModelAdmin):
    actions = [dublicate_ad]

@admin.register(models.Сategory)
class СategoryAdmin(admin.ModelAdmin):
    actions = [dublicate_ad]

@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    actions = [dublicate_ad]

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'nick', 'is_approved')
    list_editable = ['is_approved']
    search_fields = ['name', 'phone']
    readonly_fields = [
        'nick',
        'avatar',
        'text',
        'create_date',
    ]
    actions = [dublicate_ad]

@admin.register(models.Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'name', 'phone', 'is_completed')
    list_editable = ['is_completed']
    list_filter = ['name', 'phone']
    search_fields = ['name', 'phone']
    readonly_fields = [
        'name',
        'phone',
        'create_date',
    ]
    actions = [dublicate_ad]


@admin.register(models.ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('current_date', 'name', 'phone',
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
