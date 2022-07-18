from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from app import api, views
from app.schema import schema

urlpatterns = [
    path('', views.index),

    path('api/sendCallback', api.send_callback),
    path('api/sendFeedback', api.send_feedback),
    path('api/sendServices', api.send_services),
    path('api/sendPhoto', api.send_photo),
    path('api/sendPhotos', api.send_photos),

    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

    path("robots.txt", views.robots_txt),
    path("manifest.json", views.manifest),
]
