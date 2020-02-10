from django.conf import settings
from django.urls import reverse

from core.email.utils import send_email

__all__ = (
    'send_forgot_password_request',
)


def send_forgot_password_request(user):
    reset_password_path = reverse('users:reset_password', kwargs={'token': user.reset_password_token})

    subject = 'Reset your {site_name} password'.format(
        site_name=settings.SITE_NAME
    )

    send_email(
        subject=subject,
        template_name='emails/forgot_password_request.html',
        context={
            'reset_password_url': reset_password_path,
        },
        to=user.email,
    )
