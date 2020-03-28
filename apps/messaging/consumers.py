import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

import messaging.models
from messaging.utils import Firebase


class MessageConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, event):

        self.user = self.retrieve_user()
        if self.user.is_anonymous:
            await self.close()
        self.event = self.scope['url_route']['kwargs']['pk']
        self.event_room = f'event_{self.event}'

        await self.channel_layer.group_add(
            self.event_room,
            self.channel_name
        )
        await self.accept()

    async def websocket_receive(self, event):
        message_text = event.get('text', None)
        data = json.loads(message_text)
        if data['message']:
            message = await self.save_message(data['message'])
            send_data = dict(
                message=data['message'],
                sender=message.sender.pk,
                pk=message.pk,
                sender_name=message.sender.get_full_name(),
                sent_at=str(message.sent_at),
            )
            await self.firebase_notification(message)
            await self.channel_layer.group_send(
                self.event_room,
                {
                    'type': 'new_message',
                    'data': json.dumps(send_data),
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.event_room,
            self.channel_name
        )

    async def new_message(self, event):
        await self.send(text_data=event['data'])

    async def firebase_notification(self, message):
        firebase_data = dict(
            message=message.message,
            event_id=message.event.pk,
            full_name=self.user.get_full_name(),
            avatar=self.user.avatar.url if self.user.avatar else '',
        )
        users = message.event.users.all()
        user = users[1].device_id if users[0].device_id == self.user.pk else users[0].device_id
        registration_ids = [user]
        await Firebase().send_message(firebase_data, registration_ids, 1)

    def retrieve_user(self):
        return self.scope['user']

    @database_sync_to_async
    def save_message(self, message):
        event = messaging.models.Event.objects.get(pk=self.event, resolved=False)
        return messaging.models.Message.objects.create(
            event=event,
            sender=self.user,
            message=message,
        )
