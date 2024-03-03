import requests
from app import services
from django.conf import settings

SMSAERO_API_KEY = settings.SMSAERO_API_KEY
EMAIL = settings.EMAIL

def my_scheduled_job():
    print('my_scheduled_job start')
    # requests.get('http://127.0.0.1:8000')

    services.sms_sender.send_sms()
    url = f'https://{EMAIL}:{SMSAERO_API_KEY}@gate.smsaero.ru/v2/' + 'sms/send'
    params = {
        'number': '+79618228448',
        'text': 'Это тестовое сообщение, отправляю сам себе',
        'sign': 'SMS Aero'
    }

    requests.get(url, params)
    print('my_scheduled_job end')

    return 'my_scheduled_job end 2'
