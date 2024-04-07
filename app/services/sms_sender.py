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
    
    def run(self):
        logger.info('run start')

        def run_checkers():
            self.run_long_wait_checker()
            logger.info('run finish')

        t = Thread(target=run_checkers)
        t.start()
    
    def run_long_wait_checker(self):
        time.sleep(5)
        logger.info(f'run_long_wait_checker start')
        clients = models.Client.objects.filter(is_blocked=False, is_notificate=True)

        for client in clients:
            client_last_order = models.Order.objects.filter(client__id=client.id).last()

            if not client_last_order:
                continue
            
            order_services = client_last_order.services.all()

            for order_service in order_services:
               if not order_service.service.category.is_notificate:
                   continue

            self.check_and_send_sms_for_long_wait(client, client_last_order)

        logger.info(f'run_long_wait_checker finish')
    
    def check_and_send_sms_for_long_wait(self, client, last_order):
        last_order_date = last_order.update_date
        order_delta = now() - last_order_date

        if not client.phone:
            return

        message = ''

        if order_delta.days == 60:
            message = 'Здравствуйте, напоминаем Вам, что регулярный уход за питомцем это залог его комфортной жизнедеятельности, не забудьте записаться, с уважением салон ГрумЛета'
        elif order_delta.days == 90:
            message = 'Здравствуйте, мы заметили, что Вы давно не записывали своего питомца, пора наводить красоту, регулярный уход за питомцем это залог его комфортной жизнедеятельности, с уважением салон ГрумЛета'
        elif order_delta.days == 21:
            message = 'Здравствуйте, пора стричь когти Вашему питомцу, с уважением салон ГрумЛета'
        else:
            return

        logger.info(f'sms sender message: {message}')
        response = self.send_sms(client.phone, message)
        logger.info(f'sms sender response: {response}')

        if response and response['success']:
            logger.info(f'sms is send {client.id} {client.username} {now()}')
        else:
            logger.warn(f'sms is not send with exeption: [{response['message']}]')

sms_sender = SmsSender(SMSAERO_API_KEY, EMAIL)
