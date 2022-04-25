from django.urls import path

from app import api, views

urlpatterns = [
    path('', views.index),
    path('404', views.handle_page_not_found),

    path('api/sendCallback', api.send_callback),
    path('api/sendFeedback', api.send_feedback),
    path('api/sendServices', api.send_services),
    path('api/sendPhoto', api.send_photo),
    path('api/sendPhotos', api.send_photos),
]
