import uuid
import requests
from typing import Optional

from django.utils.text import slugify

__all__ = (
    'get_file_path',
    'RequiredAttrMeta',
)


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