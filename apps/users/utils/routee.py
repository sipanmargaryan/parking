import base64
import http.client
import json
from random import SystemRandom

from django.conf import settings

__all__ = (
    'Routee',
    'random_with_n_digits',
)


def random_with_n_digits(n):
    return "".join(SystemRandom().choice('123456789') for _ in range(n))


class Routee(object):

    def __init__(self):
        self.conn = http.client.HTTPSConnection("auth.routee.net")
        payload = "grant_type=client_credentials"
        encode_key = base64.b64encode(
            f'{settings.ROUTEE_APPLICATION_ID}:{settings.ROUTEE_APPLICATION_SECRET}'.encode("utf-8"))
        headers = {
            'authorization': f'Basic {encode_key.decode()}:',
            'content-type': "application/x-www-form-urlencoded"
        }
        self.conn.request("POST", "/oauth/token", payload, headers)

        res = self.conn.getresponse()
        data = res.read()
        data = json.loads(data.decode())
        self.access_token = data['access_token']

    def send_sms(self, phone_number: str, code: int):
        payload = dict(to=f'+{phone_number}', getPorted=True, numberValidatorId=code)
        headers = {
            'authorization': f'Bearer {self.access_token}',
            'content-type': "application/json"
        }
        self.conn.request("POST", "/validator", payload, headers)
        res = self.conn.getresponse()
        data = res.read()
        data = json.loads(data.decode())

