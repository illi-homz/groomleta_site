from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('graphql/', jwt_cookie(csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG)))),

    path('', include('app.urls'), name='main-view'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'app.views.handle_page_not_found'
