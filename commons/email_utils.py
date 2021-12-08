
from django.core.mail import send_mail
from django.conf import settings
from commons.trace_logger import trace_logger
import logging
logger = logging.getLogger(__name__)

@trace_logger
def send_mail_smtp(recipient_list, message_body,subject):
    send_mail(settings.EMAIL_SUBJECT_PREFIX+" | "+subject,message_body,settings.EMAIL_FROM,recipient_list, html_message=message_body)

@trace_logger
def send_email(recipient_list, message_body,subject):

    send_mail_smtp(recipient_list, message_body, subject)