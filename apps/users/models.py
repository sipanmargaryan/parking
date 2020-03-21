import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext as _

from core.models import Country, CarModel
from core.utils import get_file_path

__all__ = (
    'User',
    'Notification',
    'Car',
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not phone_number:
            raise ValueError('The given email must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True, default=None)
    phone_number = models.CharField(max_length=16, unique=True)
    avatar = models.ImageField(upload_to=get_file_path, blank=True)
    device_id = models.CharField(max_length=200, editable=False, null=True)
    phone_number_confirmation_token = models.CharField(max_length=12, editable=False, null=True)
    phone_number_valid_date = models.DateTimeField(null=True)
    reset_password_token = models.CharField(max_length=12, editable=False, null=True)
    reset_password_valid_date = models.DateTimeField(null=True)

    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)

    username = None

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone_number'

    @staticmethod
    def generate_phone_number_valid_date():
        return timezone.now() + timezone.timedelta(minutes=10)

    def get_avatar(self) -> str:
        if self.avatar:
            return self.avatar.url

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe()


class Notification(models.Model):
    SMS = 'sms'
    APP = 'app'
    BOTH = 'bh'
    METHODS = (
        (SMS, _('sms notification')),
        (APP, _('Application Notification')),
        (BOTH, _('Both Types')),
    )

    notification_method = models.CharField(max_length=3, choices=METHODS, default=APP)
    show_phone_number = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Car(models.Model):
    car_number = models.CharField(max_length=60, unique=True)
    color = models.CharField(max_length=15, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    car_model = models.ForeignKey(CarModel, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['car_number', 'user']),
        ]
