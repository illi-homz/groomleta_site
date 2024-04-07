import logging
from app.services import sms_sender
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def run_sms_sender():
    logger.info(f'[{now()}] start run_sms_sender')
    sms_sender.run()
    logger.info(f"[{now()}] end run_sms_sender")
