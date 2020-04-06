import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Country


class Command(BaseCommand):
    help = 'Initialize countries data'

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'json_data/countries_data.json'), 'rb') as f:
            countries = json.loads(f.read())
        for country in countries:
            make, _ = Country.objects.get_or_create(
                name=country['country_en'],
                country_code=country['country_code'],
                country_phone_code=country['phone_code'],
                flag=f'images/flags/{country["country_code"].lower()}.png'
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {country["country_en"]}'))
