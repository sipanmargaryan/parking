import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from core.models import Country
from core.utils import get_file_path, get_image_from_url


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=16, unique=True, null=True)
    avatar = models.ImageField(upload_to=get_file_path, blank=True)
    device_id = models.CharField(max_length=200, editable=False, null=True)
    reset_password_token = models.CharField(max_length=64, editable=False, null=True)
    reset_password_request_date = models.DateTimeField(null=True)

    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)

    username = None

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone_number'

    def generate_password_request_date(self):
        self.reset_password_request_date = timezone.now()

    def get_avatar(self) -> str:
        if self.avatar:
            return self.avatar.url

    def set_avatar(self, avatar_url: str):
        """
        Download image based on url an attach to user if valid.
        :param avatar_url:
        :return:
        """
        if not avatar_url:
            return

        file = get_image_from_url(avatar_url)
        if not file:
            return

        filename = avatar_url.split('/')[-1]
        if not any(filter(lambda ext: ext in filename, ['.jpeg', '.jpg', '.png'])):
            filename = 'avatar.jpeg'

        filename = get_file_path(self, filename)
        self.avatar.save(filename, file, save=True)

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe()

