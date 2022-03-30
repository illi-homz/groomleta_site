from django.urls import path

from app import api, views

urlpatterns = [
    path('', views.index),

    path('api/sendCallback', api.send_callback),
    path('api/sendMessage', api.send_message),
    path('api/sendPhoto', api.send_photo),
    path('api/sendPhotos', api.send_photos),
]
