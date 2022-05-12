import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
if __name__ == '__main__':
    subject, from_email, to = '来自www.liujiangblog.com的测试邮件', '13141391404@163.com', 'gaoziqi1999@gmail.com'
    text_content = '欢迎访问www.liujiangblog.com，！'
    html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a></p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
