import requests
from app import services
SMSAERO_API_KEY = settings.SMSAERO_API_KEY
EMAIL = settings.EMAIL

count = 0

def my_scheduled_job():
    # requests.get('http://127.0.0.1:8000')

    if count == 1:
        return

    # services.sms_sender.send_sms()
    url = f'https://{EMAIL}:{SMSAERO_API_KEY}@gate.smsaero.ru/v2/' + 'sms/send'
    params = {
        'number': '+79618228448',
        'text': 'Это тестовое сообщение, отправляю сам себе',
        'sign': 'SMS Aero'
    }

    requests.get(url, params)
    count += 1
