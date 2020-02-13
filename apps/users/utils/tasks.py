from celery import task

from .routee import Routee

__all__ = (
    'send_async_phone_code',
)


@task.task
def send_async_phone_code(phone_number: str, code: int):
    routee = Routee()
    routee.send_sms(phone_number, code)
