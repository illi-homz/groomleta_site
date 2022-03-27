import string
from django.http import HttpResponse
from django.shortcuts import render

from . import data
from . import models

def index(request):
    current_data = data.Index.data
    current_data['header']['banners'] = models.Banners.objects.all()
    current_data['ourworks'] = models.OurWorks.objects.all()
    current_data['promos'] = models.Promo.objects.all()

    questions = models.Questions.objects.all()
    for question in questions:
        punkts = question.punkts.split(';')
        punkts = [punkt.strip() for punkt in punkts if punkt]
        question.punkts = punkts
    
    current_data['questions'] = questions

    response = HttpResponse(render(request, 'Index.html', current_data))

    return response

def handle_page_not_found(request, exception):
    current_data = {
        'title': 'Hello World 404'
    }
    response = HttpResponse(render(request, 'Page404.html', current_data))

    return response
