from rest_framework import serializers

import messaging.models
from messaging.utils import Firebase

__all__ = (
    'MessageSerializer',
)


class MessageSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField()

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
