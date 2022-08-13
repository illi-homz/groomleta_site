from django.urls import path
from app import api, views
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    path('', views.index),

    path('api/sendCallback', api.send_callback),
    path('api/sendFeedback', api.send_feedback),
    path('api/sendServices', api.send_services),
    path('api/sendPhoto', api.send_photo),
    path('api/upload-master-avatar', jwt_cookie(csrf_exempt(api.upload_master_avatar))),
    path('api/sendPhotos', api.send_photos),
    path('api/logout', csrf_exempt(api.logout)),

    path("robots.txt", views.robots_txt),
    path("manifest.json", views.manifest),
]
