import requests
from app import models
from django.conf import settings
import logging
from django.utils.timezone import now
import time
from threading import Thread
import locale, datetime

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

    def send_sms(self, number = '+79618228448', text = 'Это тестовое сообщение, отправляю сам себе'):
        print('number', number)
        print('text', text)
        url = self.url + 'sms/send'
        params = {
            'number': number,
            'text': text,
            'sign': 'SMS Aero'
        }

        print('params', params)

        # return requests.get(url, params).json()

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
    
    def send_sms_to_client_by_event_create(self, client, event):
        if not client or not event:
            return
        
        locale.setlocale(locale.LC_ALL, '')
        timestamp = event.start_date.timestamp()
        date_time = datetime.datetime.fromtimestamp(timestamp)
        date_time_str = datetime.datetime.strftime(date_time, '%d %B в %H:%M')
        msg = f'Вы записаны в салон ГрумЛета на {date_time_str}'
        t = Thread(target=self.send_sms, args=[client.phone, msg])
        t.start()
    
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
                message = ''

                if notification_delta.days == 60:
                    message = 'Здравствуйте, напоминаем Вам, что регулярный уход за питомцем это залог его комфортной жизнедеятельности, не забудьте записаться, с уважением салон ГрумЛета'
                elif notification_delta.days == 90:
                    message = 'Здравствуйте, мы заметили, что Вы давно не записывали своего питомца, пора наводить красоту, регулярный уход за питомцем это залог его комфортной жизнедеятельности, с уважением салон ГрумЛета'
                else:
                    return

            response = self.send_sms(client.phone, message)

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

sms_sender = SmsSender(SMSAERO_API_KEY, EMAIL)
