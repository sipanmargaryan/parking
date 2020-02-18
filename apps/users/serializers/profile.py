from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

import users.models

__all__ = (
    'ChangePasswordSerializer',
    'ChangeAvatarSerializer',
    'AddEditCarSerializer',
    'EditUserSerializer',
    'NotificationSerializer',
)


# noinspection PyAbstractClass
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField()

    def validate_old_password(self, value):
        if self.context['user'].password and not value:
            raise serializers.ValidationError(_('Old password is required.'))

        if not self.context['user'].check_password(value):
            raise serializers.ValidationError(_('Invalid password.'))

        return value

    def validate_new_password(self, value):
        validate_password(value, self.context['user'])
        return value

    @staticmethod
    def change_password(user, password):
        user.set_password(password)
        user.save()

        return {
            'msg': _('Your password updated.')
        }


# noinspection PyAbstractClass
class ChangeAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = users.models.User
        fields = ('avatar',)


class AddEditCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = users.models.Car
        fields = ('car_number', 'car_model', 'color', )


class EditUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=181)

    class Meta:
        model = users.models.User
        fields = ('full_name', 'email')

    @staticmethod
    def validate_full_name(value):
        invalid_name_error_msg = _('Provided name is invalid.')
        try:
            first_name, last_name = (val.strip() for val in value.strip().split(' ', 1))
        except ValueError:
            raise serializers.ValidationError(invalid_name_error_msg)
        return first_name, last_name

    def update(self, instance, validated_data):
        instance.first_name, instance.last_name = validated_data['full_name']
        instance.email = validated_data['email']
        instance.save()

        return dict(full_name=validated_data['full_name'], email=validated_data['email'])


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = users.models.Notification
        fields = ('notification_method', )
