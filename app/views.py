from django.http import HttpResponse
from django.shortcuts import render

from . import data
from . import models

def index(request):
    current_data = data.Index.data
    current_data['header']['banners'] = models.Banners.objects.all()
    response = HttpResponse(render(request, 'Index.html', current_data))

    return response

def handle_page_not_found(request, exception):
    current_data = {
        'title': 'Hello World 404'
    }
    response = HttpResponse(render(request, 'Page404.html', current_data))

    return response
