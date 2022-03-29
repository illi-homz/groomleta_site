from django.contrib import admin
from . import models

def dublicate_ad(modeladmin, request, queryset):
	#клонирование выбранных Ad
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

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
	actions = [dublicate_ad]
