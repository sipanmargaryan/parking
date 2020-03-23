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
    'CarSerializer',
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
        fields = ('avatar', )


class AddEditCarSerializer(serializers.ModelSerializer):
    make_name = serializers.ReadOnlyField(source='car_model.make.name')
    make_pk = serializers.ReadOnlyField(source='car_model.make.pk')
    model = serializers.ReadOnlyField(source='car_model.name')
    pk = serializers.ReadOnlyField()

    class Meta:
        model = users.models.Car
        fields = ('pk', 'car_number', 'car_model', 'model', 'color',  'make_name',  'make_pk', )


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users.models.User
        fields = ('first_name', 'last_name', 'email', )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = users.models.Notification
        fields = ('notification_method', 'show_phone_number', )


class CarSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    make_name = serializers.ReadOnlyField(source='car_model.make.name')
    make_pk = serializers.ReadOnlyField(source='car_model.make.pk')
    model = serializers.ReadOnlyField(source='car_model.name')

    class Meta:
        model = users.models.Car
        fields = (
            'pk', 'car_number', 'color', 'model', 'car_model', 'make_pk', 'make_name', 'created',
        )
