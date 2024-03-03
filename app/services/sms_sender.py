import requests
import app
from django.conf import settings

SMSAERO_URL = settings.SMSAERO_URL
SMSAERO_API_KEY = settings.SMSAERO_API_KEY
EMAIL = settings.EMAIL

class SmsSender:
    api_key = ''
    email = ''
    url = ''

    def __init__(self, api_key, email):
        self.api_key = api_key
        self.email = email
        self.url = f'https://{email}:{api_key}@gate.smsaero.ru/v2/'

    def check_and_send_sms_for_long_wait(self):
        print('check_and_send_sms_for_long_wait', self.api_key)
        print('check_sms_status', self.check_sms_status(641208688))
        print('check_sms_status', app)
        pass

    def send_sms(self):
        url = self.url + 'sms/send'
        params = {
            'number': '+79618228448',
            'text': 'Это тестовое сообщение, отправляю сам себе',
            'sign': 'SMS Aero'
        }

        return requests.get(url, params).json()

    def check_sms_status(self, id):
        if (not id): return ''

        url = self.url + 'sms/status'
        params = {
            'id': id,
        }

        return requests.get(url, params).json()

    def balance(self):
        url = self.url + 'balance'
        return requests.get(url).json()

sms_sender = SmsSender(SMSAERO_API_KEY, EMAIL)

if __name__ == '__main__':
    sms_sender.check_and_send_sms_for_long_wait()
