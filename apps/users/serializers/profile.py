from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

import users.models

__all__ = (
    'ChangePasswordSerializer',
    'ChangeAvatarSerializer',
    'AddCarSerializer',
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


class AddCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = users.models.Car
        fields = ('car_number', 'car_model', 'color', )