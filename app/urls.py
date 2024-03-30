from django.urls import path
from app import api, views
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie
from .services import sms_sender

urlpatterns = [
    path('', views.index),
    path('oferta', views.oferta),

    path('api/sendCallback', api.send_callback),
    path('api/sendFeedback', api.send_feedback),
    path('api/sendServices', api.send_services),
    path('api/sendPhoto', api.send_photo),
    path('api/upload-master-avatar', jwt_cookie(csrf_exempt(api.upload_master_avatar))),
    path('api/upload-service-img', jwt_cookie(csrf_exempt(api.upload_service_img))),
    path('api/upload-product-img', jwt_cookie(csrf_exempt(api.upload_product_img))),
    path('api/sendPhotos', api.send_photos),
    path('api/logout', csrf_exempt(api.logout)),
    path('sms', views.run),
    # path('status/<int:pk>', views.status),
    # path('balance', views.balance),

    path("robots.txt", views.robots_txt),
    path("manifest.json", views.manifest),
]
