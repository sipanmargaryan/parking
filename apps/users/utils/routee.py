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
        conn = http.client.HTTPSConnection("auth.routee.net")
        payload = "grant_type=client_credentials"
        encode_key = base64.b64encode(
            f'{settings.ROUTEE_APPLICATION_ID}:{settings.ROUTEE_APPLICATION_SECRET}'.encode("utf-8"))
        headers = {
            'authorization': f'Basic {encode_key.decode()}:',
            'content-type': "application/x-www-form-urlencoded"
        }
        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode())
        self.access_token = data['access_token']

    def send_sms(self, phone_number: str, code: int):
        conn = http.client.HTTPSConnection("connect.routee.net")
        payload = json.dumps({
            'body': f'Your Parking Verification Code {code}',
            'to': f'+{phone_number}',
            'from': 'Parking'
        })
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-type': "application/json"
        }
        conn.request("POST", "/sms", payload, headers)



