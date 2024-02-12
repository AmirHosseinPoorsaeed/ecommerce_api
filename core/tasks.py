from celery import shared_task
from django.core.mail import send_mail
from time import sleep
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


@shared_task
def send_activation_email(user_email, url):
    subject = 'Account Activation Link'
    message = f'Activation Link http://127.0.0.1:8000/{url}' 
    from_email = settings.EMAIL_HOST_USER
    sleep(5)
    send_mail(subject, message, from_email, [user_email])


