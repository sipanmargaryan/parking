from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


from users.models import User


__all__ = (
    'LoginSerializer',
    'SignupSerializer',
)


class AuthPayload(object):
    pass


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
        fields = ('email', 'password', 'full_name', 'phone_number', )

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
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('A user with this email address already exists.'))
        return value

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
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            is_active=False,
        )
        user.set_password(validated_data['password'])
        user.save()

        # users.utils.emails.send_email_address_confirmation(user)

        return {'msg': _('Please confirm your phone number.')}
