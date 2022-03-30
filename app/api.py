from django.http import JsonResponse
import json
import requests
import os
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

mock_request = {
    'status': 'success',
    'code': 200,
    'ok': True
}

def send_callback(request):
    data = json.loads(request.body)

    callback = models.Callback.objects.create(name=data['name'], phone=data['tel'])
    callback.save()

    message = create_callback_msg(data)
    resp = requests.post(url, create_telegram_msg(message))
    response = {
        'status': 'success' if resp.ok else 'error',
        'code': resp.status_code,
        'ok': resp.ok
    }

    return JsonResponse(response)


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
