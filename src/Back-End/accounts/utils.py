import random

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import re

from django.urls import reverse


def send_mail(to, template, context):
    text_content = '''
    Thank you for using CloudLGU. Here is your verification code. Please use it to finish your operation!
    '''
    html_content = '''
    <p>
    Thank you for using CloudLGU. Here is your verification code. Please use it to finish your operation!
    Verification Code:<em>{}</em> 
    </p>
    '''.format(context['code'])
    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def send_activation_email(request, email, code):
    context = {
        'subject': f'{request}',
        # 'uri': request.build_absolute_uri(reverse('activate', kwargs={'code': code})),
        'code': code,
        'confirm_time': settings.CONFIRM_TIME
    }

    send_mail(email, 'activate_profile', context)


def send_Inform():
    text_content = '''
    Thank you for using CloudLGU. Your account has been deleted. Please connect admin(118010339@link.cuhk.edu.cn)!
    ''',
    html_content= '''
    <p>
    Thank you for using CloudLGU. Your account has been deleted. Please connect admin (118010339@link.cuhk.edu.cn)!
    </p>
    '''


    msg = EmailMultiAlternatives("Your account has been deleted.", text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def check_identification(email):
    student_pattern = re.compile(r'@link.cuhk.edu.cn')
    staff_pattern = re.compile(r'@cuhk.edu.cn')

    if student_pattern.search(email):
        return 'student'
    elif staff_pattern.search(email):
        return 'staff'
    else:
        return 'invalid'
def get_verification(bits):
    code = ""
    for i in range(bits):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch
    return code
