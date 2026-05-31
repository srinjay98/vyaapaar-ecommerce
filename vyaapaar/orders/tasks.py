from celery import shared_task

from django.core.mail import send_mail

from django.conf import settings


@shared_task
def send_order_email(user_email, order_id):

    send_mail(

        subject='Order Confirmation',

        message=(
            f'Your order #{order_id} '
            f'has been placed successfully.'
        ),

        from_email=settings.EMAIL_HOST_USER,

        recipient_list=[user_email],

        fail_silently=False,
    )