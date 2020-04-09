import uuid

from rest_framework import status
from rest_framework.exceptions import APIException

from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.conf import settings

__all__ = (
    'build_client_absolute_url',
    'get_file_path',
    'RequiredAttrMeta',
    'FoundException',
)


def build_client_absolute_url(path: str) -> str:
    domain = settings.CLIENT_DOMAIN
    url_scheme = settings.URL_SCHEME

    return path and f'{url_scheme}://{domain}{path}' or ''


def get_file_path(instance, filename: str) -> str:
    model = type(instance)
    upload_dir = '{}/{}'.format(
        slugify(model._meta.app_label),
        slugify(model.__name__)
    )

    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4(), ext)
    return 'images/{}/{}'.format(upload_dir, filename)


class RequiredAttrMeta(type):
    def __init__(cls, name, bases, clsdict):
        super().__init__(name, bases, clsdict)
        if not bases:
            return
        if not hasattr(cls, '_required_attributes'):
            return
        for attr in cls._required_attributes:
            if not hasattr(cls, attr):
                raise AttributeError(f'Attribute {attr} not present in {name}')


class FoundException(APIException):
    status_code = status.HTTP_302_FOUND
    default_detail = _('Please confirm your phone number.')

    def __init__(self, default_detail=None, detail=None, code=None):
        if default_detail:
            self.default_detail = default_detail
        super(FoundException, self).__init__(detail, code)
