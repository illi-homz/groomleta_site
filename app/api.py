from unicodedata import name
from django.http import JsonResponse
import json
import requests
import os
import re
from . import models

botToken = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
url = f'https://api.telegram.org/bot{botToken}/sendMessage'
url_photo = f'https://api.telegram.org/bot{botToken}/sendPhoto'
url_media_group = f'https://api.telegram.org/bot{botToken}/sendMediaGroup'


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
    msg += f'#Клиент: ${data["name"]} ${data["lastname"]}\n'
    msg += f'#Комментарий: ${data["comment"]}'

    return msg

def concatFio(data):
    name = ''

    if data["name"]: name += data["name"]
    if data["lastname"]: name += data["lastname"]

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
    response = {
        'status': 'success' if resp.ok else 'error',
        'code': resp.status_code,
        'ok': resp.ok
    }

    return JsonResponse(response)
    # return JsonResponse(mock_response)

def send_feedback(request):
    data = json.loads(request.body)

    feedback = models.Feedback.objects.create(nick=concatFio(data), text=data["comment"])
    feedback.save()

    message = create_feedback_msg(data)
    # print('message', message)
    resp = requests.post(url, create_telegram_msg(message))
    response = {
        'status': 'success' if resp.ok else 'error',
        'code': resp.status_code,
        'ok': resp.ok
    }

    return JsonResponse(response)
    # return JsonResponse(mock_response)

def send_message(request):
    message = json.loads(request.body)
    resp = requests.post(url, create_telegram_msg(message))
    response = {
        'status': 'success' if resp.ok else 'error',
        'code': resp.status_code,
        'ok': resp.ok
    }

    return JsonResponse(response)


def send_photo(request):
    # photo = request.files.getlist('file')[0]
    # params = {'chat_id': chat_id}
    # files = {'photo': photo}
    # r = requests.post(url_photo, params, files=files)
    # print('photoSender', r.json())
    return JsonResponse({'status': 'success'})


def send_photos(request):
    # files = request.files.getlist('files')
    # params = {
    #     'chat_id': chat_id,
    #     'media': [{'type': 'photo', 'media': f'attach://{file.filename}'} for file in files]
    # }

    # params['media'] = json.dumps(params['media'])

    # current_files = {}
    # for file in files:
    #     current_files[file.filename] = file

    # r = requests.post(url_media_group, params, files=current_files)
    # print('mediaGroupSender', r.json())
    return JsonResponse({'status': 'success'})
