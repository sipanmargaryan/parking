import uuid
import requests
from typing import Optional

from django.utils.text import slugify
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

__all__ = (
    'get_file_path',
    'get_image_from_url',
    'RequiredAttrMeta',
)


def get_file_path(instance, filename: str) -> str:
    model = type(instance)
    upload_dir = '{}/{}'.format(
        slugify(model._meta.app_label),
        slugify(model.__name__)
    )

    upload_dir = upload_dir.replace('ad', 'classified')
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4(), ext)
    return 'images/{}/{}'.format(upload_dir, filename)


def get_image_from_url(url: str) -> Optional[File]:
    response = requests.get(url)

    if response.status_code == 200:

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()

        return File(img_temp)


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