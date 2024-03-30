import logging
from app.services import sms_sender
from threading import Thread
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def run_sms_sender():
    logger.info(f'start run_sms_sender {now()}')
    sms_sender.run()
    logger.info(f"end run_sms_sender {now()}")
