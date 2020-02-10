import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialize countries data'

    def handle(self, *args, **options):
        pass
