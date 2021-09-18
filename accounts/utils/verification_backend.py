import random
import requests

from django.core.mail import send_mail
from django.conf import settings

from celery.task import task

URL = 'https://api.kavenegar.com/v1/{token}/sms/send.json'.format(token=settings.SMS_TOKEN)


def generate_code():
    return str(random.randint(10000, 99999))


@task(name='Send Verification Email')
def send_verification_email(email, value):
    message = 'باعرض سلام کد تایید شما {} میباشد.'.format(value)
    subject = 'کد فعالسازی'
    recipient_list = [email]
    send_mail(message=message, subject=subject, recipient_list=recipient_list, from_email='Social_Media',
              fail_silently=False)
    return 'Verification Email Sent Successfully'


@task(name='Send Verification SMS')
def send_verification_sms(value):
    message = 'باعرض سلام کد تایید شما {} میباشد.'.format(value)
    data = {
        'receptor': '09302658144',
        'message': message
    }
    requests.post(url=URL, data=data)
    return 'Code Was sent successfully'
