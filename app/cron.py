import logging
from app.services import sms_sender

logger = logging.getLogger(__name__)

def check_and_send_sms_for_long_wait():
    logger.info("start check_and_send_sms_for_long_wait")
    sms_sender.check_and_send_sms_for_long_wait()
    logger.info("end check_and_send_sms_for_long_wait")
