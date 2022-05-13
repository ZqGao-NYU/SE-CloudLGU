import random

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import re



def send_mail(to, context):
    """Send verification email with verification code to the user. Send with HTML format."""
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
        'code': code,
        'confirm_time': settings.CONFIRM_TIME
    }

    send_mail(email, context)


def send_inform(to):
    """If the user's account is deleted by the administrator, an email will be sent to that user."""
    text_content = '''
    Thank you for using CloudLGU. Your account has been deleted. Please connect admin(118010339@link.cuhk.edu.cn)!
    '''
    html_content = '''
    <p>
    Thank you for using CloudLGU. Your account has been deleted. Please connect admin (118010339@link.cuhk.edu.cn)!
    </p>
    '''

    msg = EmailMultiAlternatives("Your account has been deleted.", text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def check_identification(email):
    """Use email's pattern to check the user's identity

    Keyword Argument:
    email: User's Email
    """
    student_pattern = re.compile(r'@link.cuhk.edu.cn')  # Student's email ends with @link.cuhk.edu.cn
    staff_pattern = re.compile(r'@cuhk.edu.cn')  #  Staff's email ends with @cuhk.edu.cn

    if student_pattern.search(email):
        return 'student'
    elif staff_pattern.search(email):
        return 'staff'
    else:
        return 'invalid'


def get_verification(bits):
    """Generate the code with specified bits. E.g. Generate a 6-bit verification code with get_verification(6)"""
    code = ""
    for i in range(bits):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch
    return code
