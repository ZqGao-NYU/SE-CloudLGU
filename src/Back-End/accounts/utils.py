from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import re

from django.urls import reverse


def send_mail(to, template, context):
    html_content = render_to_string(f'emails/{template}.html', context)
    text_content = render_to_string(f'emails/{template}.txt', context)
    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def send_activation_email(request, email, code):
    context = {
        'subject': 'Profile activation',
        'uri': request.build_absolute_uri(reverse('activate', kwargs={'code': code})),
    }

    send_mail(email, 'activate_profile', context)


def check_identification(email):
    student_pattern = re.compile(r'@link.cuhk.edu.cn')
    staff_pattern = re.compile(r'@cuhk.edu.cn')

    if student_pattern.search(email):
        return 'student'
    elif staff_pattern.search(email):
        return 'staff'
    else:
        return 'invalid'
