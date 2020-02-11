from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from core.models import Country
from users.models import User


__all__ = (
    'LoginSerializer',
    'SignupSerializer',
    'ConfirmPhoneNumberSerializer',
    'ForgotPasswordSerializer',
    'ResetPasswordSerializer',
)


class AuthPayload(object):

    @staticmethod
    def get_auth_payload(user: User, additional_data: dict = None) -> dict:

        def get_avatar(avatar):
            if avatar:
                return avatar.url

            return None

        refresh = RefreshToken.for_user(user)

        payload = {
            'user': {
                'pk': user.pk,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar': get_avatar(user.avatar),
                'country': user.country.name,
            },
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }

        if additional_data:
            payload = {**payload, **additional_data}

        return payload


# noinspection PyAbstractClass
class LoginSerializer(serializers.Serializer, AuthPayload):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, validated_data):
        return self.get_auth_payload(self.get_user(**validated_data))

    @staticmethod
    def get_user(phone_number: str, password: str) -> User:
        invalid_credentials = _('Invalid login credentials.')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(invalid_credentials)

        if not user.check_password(password):
            raise serializers.ValidationError(invalid_credentials)

        return user


class SignupSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=181)

    class Meta:
        model = User
        fields = ('password', 'full_name', 'phone_number', )

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    @staticmethod
    def validate_full_name(value):
        invalid_name_error_msg = _('Provided name is invalid.')
        try:
            first_name, last_name = (val.strip() for val in value.strip().split(' ', 1))
        except ValueError:
            raise serializers.ValidationError(invalid_name_error_msg)
        return first_name, last_name

    @staticmethod
    def validate_phone_number(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('A user with this phone_number already exists.'))
        return value

    def create(self, validated_data):
        first_name, last_name = validated_data['full_name']

        user = User(
            first_name=first_name,
            last_name=last_name,
            country=Country.objects.get(name=settings.DEFAULT_COUNTRY),
            phone_number=validated_data['phone_number'],
            is_active=False,
        )
        user.set_password(validated_data['password'])
        user.save()

        # users.utils.emails.send_email_address_confirmation(user)

        return {'msg': _('Please confirm your phone number.')}


# noinspection PyAbstractClass
class ConfirmPhoneNumberSerializer(serializers.Serializer, AuthPayload):
    token = serializers.CharField()

    def validate_token(self, value):
        # noinspection PyAttributeOutsideInit
        self.user = User.objects.filter(phone_confirmation_token=value).first()
        if not self.user:
            raise serializers.ValidationError(_('Invalid token.'))
        return value

    def create(self, validated_data):
        self.user.is_active = True
        self.user.phone_confirmation_token = None
        self.user.save()

        return self.get_auth_payload(
            user=self.user,
            additional_data={
                'msg': _('You have successfully confirmed you phone number.')
            },
        )


# noinspection PyAbstractClass
class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.filter(phone_number=validated_data['phone_number']).first()
        if user:
            user.generate_password_request_date()
            user.reset_password_token = User.generate_token()
            user.save()

            # users.utils.emails.send_forgot_password_request(user)

        return {'msg': _('Please check your phone number.')}


# noinspection PyAbstractClass
class ResetPasswordSerializer(serializers.Serializer, AuthPayload):
    token = serializers.CharField()
    password = serializers.CharField()

    def validate_token(self, value):
        # noinspection PyAttributeOutsideInit
        self.user = User.objects.filter(reset_password_token=value).first()

        if not self.user:
            raise serializers.ValidationError(_('Invalid Reset Password Code.'))

        return value

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def create(self, validated_data):
        self.user.reset_password_token = None
        self.user.reset_password_request_date = None
        self.user.is_active = True
        self.user.set_password(validated_data['password'])

        self.user.save()

        return self.get_auth_payload(self.user)
