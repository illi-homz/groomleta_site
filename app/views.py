from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from . import data
from . import models

def index(request):
    current_data = data.Index.data
    current_data['header']['banners'] = models.Banner.objects.all()
    current_data['ourworks'] = models.OurWork.objects.all()
    current_data['oursalon'] = models.OurSalon.objects.all()
    current_data['promos'] = models.Promo.objects.all()
    current_data['feedbacks'] = models.Feedback.objects.filter(is_approved=True)
    current_data['services'] = {}
    current_data['services']['categories'] = models.Сategory.objects.all()
    current_data['services']['breeds'] = models.Breed.objects.all()
    current_data['services']['services_list'] = models.Service.objects.all()

    questions = models.Question.objects.all()
    for question in questions:
        punkts = question.punkts.split('\n')
        punkts = [punkt.strip() for punkt in punkts if punkt]
        question.punkts = punkts
    current_data['questions'] = questions

    return HttpResponse(render(request, 'Index.html', current_data))

def handle_page_not_found(request, exception):
    current_data = data.Page404.data
    response = HttpResponse(render(request, 'Page404.html', current_data))

    return response

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Crawl-delay: 5",
        "Host: groomleta.ru",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def manifest(request):
    return JsonResponse(data.manifest.data)
