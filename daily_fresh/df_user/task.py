import time
from celery import task
from django.core.mail import send_mail
from django.conf import settings

@task
def send_register_mail(username, password, email):
    msg = 'hhh' + username + '<br>zzz' + password
    send_mail('欢迎信息', '', settings.EMAIL_FROM, [email, ], html_message=msg)
    time.sleep(2)
