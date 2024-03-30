from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from app import data, models, services

def index(request):
    prefix = '#'
    header_links_filters = []
    promos = models.Promo.objects.all()

    if not promos.count():
        header_links_filters.append(f'{prefix}promo')

    current_data = data.Index.get_data(prefix, header_links_filters)
    current_data['header']['banners'] = models.Banner.objects.all()
    current_data['ourworks'] = models.OurWork.objects.all()
    current_data['oursalon'] = models.OurSalon.objects.all()
    current_data['promos'] = promos
    current_data['feedbacks'] = models.Feedback.objects.filter(is_approved=True)
    current_data['services'] = {}
    current_data['services']['categories'] = models.Category.objects.all()
    current_data['services']['breeds'] = models.Breed.objects.filter(show=True)
    current_data['services']['services_list'] = models.Service.objects.order_by('breed__id')

    questions = models.Question.objects.all()
    for question in questions:
        punkts = question.punkts.split('\n')
        punkts = [punkt.strip() for punkt in punkts if punkt]
        question.punkts = punkts
    current_data['questions'] = questions

    return HttpResponse(render(request, 'Index.html', current_data))

def oferta(request):
    prefix = '/#'
    header_links_filters = []
    promos = models.Promo.objects.all()

    if not promos.count():
        header_links_filters.append(f'{prefix}promo')

    current_data = data.Index.get_data(prefix, header_links_filters)
    oferta_text = data.Oferta.oferta_text
    punkts = oferta_text.split('\n')

    current_data['oferta_text'] = [punkt.strip() for punkt in punkts]
    return HttpResponse(render(request, 'Oferta.html', current_data))

def handle_page_not_found(request, exception):
    current_data = data.Page404.data
    response = HttpResponse(render(request, 'Page404.html', current_data))

    return response

def run(request):
    services.sms_sender.run()
    return JsonResponse({})

# def status(request, pk):
#     json = services.sms_sender.check_sms_status(pk)
#     return JsonResponse(json)

# def balance(request):
#     json = services.sms_sender.balance()
#     return JsonResponse(json)

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Crawl-delay: 5",
        "Host: groomleta.ru",
        "Disallow: /admin",

        "User-Agent: *",
        "Disallow: /crm",

        "User-Agent: *",
        "Disallow: /oferta",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def manifest(request):
    return JsonResponse(data.manifest.data)
