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

@admin.register(models.OurSalon)
class OurSalonAdmin(admin.ModelAdmin):
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
    list_per_page = 20

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_editable = ['title']
    actions = [dublicate_ad]

@admin.register(models.Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'show')
    list_editable = ['title', 'show']
    actions = [dublicate_ad]

@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'breed', 'category', 'animal', 'price', 'image_tag', 'is_notificate')
    list_editable = ['title', 'breed', 'animal', 'price', 'is_notificate']
    list_filter = ['title', 'animal', 'category']
    search_fields = ['title']
    exclude = ('is_active',)
    actions = [dublicate_ad]
    list_per_page = 20
    ordering = ('id',)

    def image_tag(self, obj):
        return format_html(f'<img width="50" src="{obj.img.url}" />')

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
    list_per_page = 20
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
    list_per_page = 20
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
    list_per_page = 20
    ordering = ('id',)

@admin.register(models.Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'lastname', 'phone', 'avatar', 'post', 'is_active']
    list_editable = ['username', 'lastname', 'phone', 'post', 'is_active']
    search_fields = ['username', 'lastname', 'phone', 'is_active']
    readonly_fields = ['create_date', 'update_date']
    list_per_page = 20
    ordering = ('id',)
    actions = [dublicate_ad]

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date', 'client', 'get_services', 'master', 'comment']
    list_editable = ['title', 'client', 'master']
    search_fields = ['title']
    readonly_fields = ['create_date', 'update_date']
    list_per_page = 20
    ordering = ('id',)
    actions = [dublicate_ad]

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'vendor_code', 'count', 'price']
    list_editable = ['vendor_code', 'count', 'price']
    search_fields = ['title', 'vendor_code']
    readonly_fields = ['create_date', 'update_date']
    exclude = ('is_active',)
    list_per_page = 20
    ordering = ('title',)
    actions = [dublicate_ad]

@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'lastname', 'phone', 'image_tag', 'is_blocked', 'is_notificate']
    list_editable = ['username', 'lastname', 'phone', 'is_blocked', 'is_notificate']
    search_fields = ['username', 'lastname', 'phone']
    readonly_fields = ['create_date', 'update_date']
    exclude = ('is_active',)
    list_per_page = 20
    ordering = ('id',)
    actions = [dublicate_ad]

    def image_tag(self, obj):
        return format_html('<img width="100" src="{}" />'.format(obj.avatar.url)) if obj.avatar else ''

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'create_date', 'update_date', 'is_success']
    list_editable = ['is_success']
    search_fields = ['price', 'create_date']
    readonly_fields = ['create_date', 'update_date']
    exclude = ('is_active',)
    list_per_page = 20
    ordering = ('-create_date',)
    actions = [dublicate_ad]

@admin.register(models.OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'count']
    list_per_page = 20
    actions = [dublicate_ad]
