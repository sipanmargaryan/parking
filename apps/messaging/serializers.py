from rest_framework import serializers

from django.utils.translation import gettext as _

import messaging.models
from messaging.utils import Firebase

__all__ = (
    'MessageSerializer',
    'ResolveEventSerializer',
)


# noinspection PyAbstractClass
class MessageSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()
    message = serializers.CharField()
    image = serializers.ImageField()

    class Meta:
        model = messaging.models.Message
        fields = ('message', 'image', 'car_id')

    @staticmethod
    def save_message(event, sender, message):

        if event.resolved:
            return {
                'msg': 'Chat is blocked.'
            }

        messaging.models.Message.objects.create(
            event=event,
            message=message,
            sender=sender
        )

        data = {
            'message': message,
            'full_name': sender.get_full_name(),
            'avatar': sender.avatar.url if sender.avatar else '',
        }

        users = event.users.all()
        registration_ids = [users[0].device_id, users[1].device_id]
        Firebase().send_message(data, registration_ids, 1)


class ResolveEventSerializer(serializers.ModelSerializer):
    event = serializers.IntegerField(write_only=True)

    class Meta:
        model = messaging.models.Event
        fields = ('event', )

    @staticmethod
    def resolve_event(event):
        event.resolved = True
        event.save()

        return {
            'msg': _('Chat has been resolved.')
        }
