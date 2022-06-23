from django.urls import path

from app import api, views

urlpatterns = [
    path('', views.index),

    path('api/sendCallback', api.send_callback),
    path('api/sendFeedback', api.send_feedback),
    path('api/sendServices', api.send_services),
    path('api/sendPhoto', api.send_photo),
    path('api/sendPhotos', api.send_photos),

    path("robots.txt", views.robots_txt),
    path("manifest.json", views.manifest),
]
