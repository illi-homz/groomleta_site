import requests
from app import models
from django.conf import settings
import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)

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
        clients = models.Client.objects.filter(is_blocked=False)

        for client in clients:
            client_last_order = models.Order.objects.filter(client__id=client.id).last()

            if not client_last_order:
                return

            client_last_order_date = client_last_order.update_date
            order_delta = now() - client_last_order_date

            if order_delta.days < 60:
                return

            client_last_notification = models.SmsNotification.objects.filter(user__id=client.id, success=True).last()

            if client_last_notification:
                client_last_notification_date = client_last_notification.created
                notification_delta = now() - client_last_notification_date

                if notification_delta.days < 60:
                    return

            response = self.send_sms(client.phone, 'какое то текстовое сообщение')

            if response['success']:
                logger.info(f'sms is send {client.id} {client.username} {now()}')
                models.SmsNotification.objects.create(user=client, success=True)
            else:
                models.SmsNotification.objects.create(
                    user=client,
                    success=False,
                    error_message=response['success']
                )
                logger.warn(f'sms is not send with exeption: [{response['message']}]')

    def send_sms(self, number = '+79618228448', text = 'Это тестовое сообщение, отправляю сам себе'):
        print('number', number)
        print('text', text)
        url = self.url + 'sms/send'
        params = {
            'number': number,
            'text': text,
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
