from django.contrib import admin
from . import models

def dublicate_ad(modeladmin, request, queryset):
	#клонирование выбранных Ad
	for el in queryset:
		el.pk = None
		el.save()

dublicate_ad.short_description = "Дублировать объект"

@admin.register(models.Banners)
class BannersAdmin(admin.ModelAdmin):
	actions = [dublicate_ad]

@admin.register(models.OurWorks)
class OurWorksAdmin(admin.ModelAdmin):
	actions = [dublicate_ad]

@admin.register(models.Questions)
class QuestionsAdmin(admin.ModelAdmin):
	actions = [dublicate_ad]

@admin.register(models.Promo)
class PromoAdmin(admin.ModelAdmin):
	actions = [dublicate_ad]
