from rest_framework import generics, permissions, status
from rest_framework.response import Response

from django.http import Http404

import users.models
import messaging.models

from .serializers import *  # noqa

__all__ = (
    'SendMessageAPIView',
)


class SendMessageAPIView(generics.CreateAPIView):
    queryset = messaging.models.Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    status_code = status.HTTP_201_CREATED

    def get_object(self, car_id):
        car = (
            users.models.Car.objects
            .filter(pk=car_id)
            .exclude(user=self.request.user)
            .select_related('user')
            .first()
        )
        if not car or not car.user:
            raise Http404

        return car

    def get_or_create_event(self, car):
        user = self.request.user

        event = messaging.models.Event.objects.filter(car=car, users=user).prefetch_related('users').first()
        if not event:
            event = messaging.models.Event.objects.create(car=car)
            event.users.set([user, car.user])

        return event

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = self.get_object(serializer.validated_data['car_id'])
        event = self.get_or_create_event(car)
        response = serializer.save_message(
            event=event,
            sender=self.request.user,
            message=serializer.validated_data['message']
        )
        if response:
            self.status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=self.status_code)
