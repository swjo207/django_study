from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    """
    주문이 생성되면 이메일로 주문자에게 알린다.
    """
    order = Order.objects.get(id=order_id)
    subject = '주문 번호. {}'.format(order.id)
    message = 'Dear {}, \n\n 당신의 주문이 성공적으로 이루어졌습니다. 당신의 주문 ID는 {} 입니다.'.format(order.first_name,order.id)
    mail_sent = send_mail(subject,message,'admin@myshop.com',[order.email])
    return mail_sent

