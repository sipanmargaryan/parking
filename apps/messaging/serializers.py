from rest_framework import serializers

from django.utils.translation import gettext as _
from django.contrib.humanize.templatetags.humanize import naturaltime

import messaging.models
from messaging.utils import Firebase

__all__ = (
    'MessageSerializer',
    'InboxSerializer',
    'InboxDetailSerializer',
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


class InboxSerializer(serializers.ModelSerializer):
    thread = serializers.SerializerMethodField()

    class Meta:
        model = messaging.models.Message
        fields = (
            'thread',
        )

    @staticmethod
    def get_thread(message):
        return {
            'pk': message.event.pk,
            'message': message.message,
            'resolved': message.event.resolved,
            'sent_at': naturaltime(message.sent_at),
        }


class InboxDetailSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = messaging.models.Message
        fields = (
            'pk', 'message', 'sent_at', 'sender', 'sender_name'
        )

    @staticmethod
    def get_sender(message):
        return message.sender.pk

    @staticmethod
    def get_sender_name(message):
        return message.sender.get_full_name()


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
