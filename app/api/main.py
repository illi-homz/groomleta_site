from django.http import JsonResponse, HttpResponseServerError
import json
import requests
import os
import re
from app import models
from django.utils.timezone import datetime, localdate, now
from django.forms.models import model_to_dict
from graphql_jwt.utils import get_http_authorization, get_payload, get_user_by_payload
from graphql_jwt.exceptions import PermissionDenied

import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.services import create_response

botToken = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
url = f'https://api.telegram.org/bot{botToken}/sendMessage'
url_photo = f'https://api.telegram.org/bot{botToken}/sendPhoto'
url_media_group = f'https://api.telegram.org/bot{botToken}/sendMediaGroup'

mock_reaponse = {
    'status': 'success',
    'code': 200,
    'ok': True
}


def create_telegram_msg(msg):
    print('create_telegram_msg', msg)
    return {'chat_id': chat_id, 'text': msg, 'parse_mode': 'markdown'}


def create_callback_msg(data):
    msg = '*Заказ звонка*\n\n'
    msg += f'#Клиент: {data["name"]}\n'
    msg += f'#Тел: {data["tel"]}'

    return msg


def create_feedback_msg(data):
    msg = '*Отзыв*\n\n'
    msg += f'#Клиент: {data["name"]} {data["lastname"]}\n'
    msg += f'#Комментарий: {data["comment"]}'

    return msg


def create_services_msg(data):
    [year, month, day] = data['date'].split('-')

    msg = '*Запись*\n\n'
    msg += f'#Клиент: {data["name"]} {data["lastname"]}\n'
    msg += f'#Тел: {data["tel"]}\n'
    msg += f'#Дата: {day}.{month}.{year}\n'
    msg += f'#Комментарий: {data["comment"]}\n'
    msg += f'#Услуги: {data["services"]}\n'
    msg += f'#Мин цена: {data["price"]}'

    return msg


def concatFio(data):
    name = ''

    if data["name"]:
        name += data["name"]
    if data["lastname"]:
        name += f' {data["lastname"]}'

    return name


mock_response = {
    'status': 'success',
    'code': 200,
    'ok': True
}


def send_callback(request):
    data = json.loads(request.body)

    phone = re.sub('[^0-9]', '', data['tel'])
    callback = models.Callback.objects.create(name=data['name'], phone=phone)
    callback.save()

    message = create_callback_msg(data)
    resp = requests.post(url, create_telegram_msg(message))

    return JsonResponse(create_response(resp))


def send_feedback(request):
    data = json.loads(request.body)

    feedback = models.Feedback.objects.create(
        nick=concatFio(data), text=data['comment'])
    feedback.save()

    message = create_feedback_msg(data)
    resp = requests.post(url, create_telegram_msg(message))

    return JsonResponse(create_response(resp))


def send_services(request):
    try:
        data = json.loads(request.body)
        service = models.ServiceRecord.objects.create(
            name=concatFio(data),
            phone=data['tel'],
            min_price=data['price'],
            services=data['services'],
            comment=data['comment'],
            current_date=data['date']
        )
        service.save()

        message = create_services_msg(data)
        resp = requests.post(url, create_telegram_msg(message))

        return JsonResponse(create_response(resp))
    except:
        return HttpResponseServerError('Ошибка отправки данных')


def send_photo(request):
    try:
        photo = request.FILES.getlist('file')[0]
        params = {'chat_id': chat_id}
        files = {'photo': photo}
        resp = requests.post(url_photo, params, files=files)

        return JsonResponse(create_response(resp))
    except:
        return HttpResponseServerError('Невозможно отправить фото')


def send_photos(request):
    try:
        files = request.FILES.getlist('files')
        params = {
            'chat_id': chat_id,
            'media': [{'type': 'photo', 'media': f'attach://{file.name}'} for file in files]
        }
        params['media'] = json.dumps(params['media'])
        current_files = {}

        for file in files:
            current_files[file.name] = file

        resp = requests.post(url_media_group, params, files=current_files)

        return JsonResponse(create_response(resp))
    except:
        return HttpResponseServerError('Невозможно отправить фото')


def upload_master_avatar(request):
    token = get_http_authorization(request)

    try:
        payload = get_payload(token)
        get_user_by_payload(payload)
    except:
        return HttpResponseServerError(PermissionDenied)

    master_id = request.POST['id']
    avatar = request.FILES.getlist('file')[0]
    master = models.Master.objects.get(pk=master_id)
    master.avatar = avatar
    master.save()

    return JsonResponse({
        'status': 'success',
        'code': 200,
        'ok': True
    })

def upload_service_img(request):
    token = get_http_authorization(request)

    try:
        payload = get_payload(token)
        get_user_by_payload(payload)
    except:
        return HttpResponseServerError(PermissionDenied)

    service_id = request.POST['id']
    img = request.FILES.getlist('file')[0]
    service = models.Service.objects.get(pk=service_id)
    service.img = img
    service.save()

    return JsonResponse({
        'status': 'success',
        'code': 200,
        'ok': True
    })

def upload_product_img(request):
    token = get_http_authorization(request)

    try:
        payload = get_payload(token)
        get_user_by_payload(payload)
    except:
        return HttpResponseServerError(PermissionDenied)

    product_id = request.POST['id']
    img = request.FILES.getlist('file')[0]
    product = models.Product.objects.get(pk=product_id)
    product.img = img
    product.save()

    return JsonResponse({
        'status': 'success',
        'code': 200,
        'ok': True
    })
