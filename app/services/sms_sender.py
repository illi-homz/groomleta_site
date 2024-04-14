import requests
from app import models
from django.conf import settings
import logging
from django.utils.timezone import now
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
        url = self.url + 'sms/send'
        params = {
            'number': number,
            'text': text,
            'sign': 'SMS Aero'
        }

        try:
            return requests.get(url, params).json()
        except Exception as e:
            logger.warn(f'send_sms exeption: {e}')

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

    def send_sms_to_client_by_order_create(self, client):
        if not client:
            return
        
        locale.setlocale(locale.LC_ALL, '')
        msg = 'Спасибо, что выбрали салон ГрумЛета! Ваш отзыв поможет нам стать лучше https://yandex.ru/maps/org/2393762986932'
        t = Thread(target=self.send_sms, args=[client.phone, msg])
        t.start()
    
    def run(self):
        logger.info(f'[{now()}] run start')

        def run_checkers():
            self.run_long_wait_checker()
            logger.info(f'[{now()}] run finish')

        t = Thread(target=run_checkers)
        t.start()
    
    def run_long_wait_checker(self):
        clients = models.Client.objects.filter(is_blocked=False, is_notificate=True)

        for client in clients:
            client_last_order = models.Order.objects.filter(client__id=client.id).last()
            client_last_upcoming_events_count = models.Event.objects.filter(
                client__id=client.id,
                start_date__gte=now()
            ).count()

            if not client_last_order or client_last_upcoming_events_count:
                continue
            
            order_services = client_last_order.services.all()
            is_not_notificate_services_count = order_services.filter(service__is_notificate=False).count()

            if is_not_notificate_services_count:
                continue

            self.check_and_send_sms_for_long_wait(client, client_last_order)
    
    def check_and_send_sms_for_long_wait(self, client, last_order):
        logger.info(f'check_and_send_sms_for_long_wait start')
        if not client.phone:
            return

        last_order_date = last_order.update_date
        order_delta = now() - last_order_date
        days = order_delta.days
        logger.info(f'days: {days}')
        message = ''

        if days == 60:
            message = 'Здравствуйте, напоминаем Вам, что регулярный уход за питомцем это залог его комфортной жизнедеятельности, не забудьте записаться! С уважением салон ГрумЛета'
        # elif days == 90:
        #     message = 'Здравствуйте, мы заметили, что Вы давно не записывали своего питомца, пора наводить красоту, регулярный уход за питомцем это залог его комфортной жизнедеятельности, с уважением салон ГрумЛета'
        # elif days == 21:
        #     message = 'Здравствуйте, пора стричь когти Вашему питомцу, с уважением салон ГрумЛета'
        else:
            return


        response = self.send_sms(client.phone, message)
        logger.info(f'[{now()}] sms sender response: {response}')

        if response and response['success']:
            logger.info(f'[{now()}] sms is send {client.id} {client.username}')
        else:
            logger.warn(f'[{now()}] sms is not send with exeption')

sms_sender = SmsSender(SMSAERO_API_KEY, EMAIL)
