from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response

from django.http import Http404

import users.models
import messaging.models

from .serializers import *  # noqa

__all__ = (
    'SendMessageAPIView',
    'InboxAPIView',
    'InboxDetailAPIView',
    'ResolveEventAPIView',
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
            .exclude(user=self.request.user, event__resolved=True)
            .select_related('user')
            .first()
        )
        if not car or not car.user:
            raise Http404

        return car

    def create_event(self, **kwargs):
        user = self.request.user
        event = messaging.models.Event.objects.create(**kwargs)
        event.users.set([user, kwargs['car'].user])

        return event

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = self.get_object(serializer.validated_data['car_id'])
        event_data = dict(car=car, image=serializer.validated_data.get('image', None))
        event = self.create_event(**event_data)
        response = serializer.save_message(
            event=event,
            sender=self.request.user,
            message=serializer.validated_data['message']
        )
        if response:
            self.status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=self.status_code)


class InboxAPIView(generics.ListAPIView):
    queryset = messaging.models.Message.objects.all()
    serializer_class = InboxSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        events = messaging.models.Event.objects.filter(users=user)
        return (messaging.models.Message.objects
                .filter(event__pk__in=events)
                .distinct('event')
                .select_related('event__car')
                .order_by('event', '-sent_at'))


class InboxDetailAPIView(generics.ListAPIView):
    queryset = messaging.models.Message.objects.all()
    serializer_class = InboxDetailSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        event_id = self.kwargs.get('event')
        return (
            self.queryset
            .filter(event=event_id, event__users__pk=self.request.user.pk)
            .select_related('sender')
            .order_by('-sent_at')
        )


class ResolveEventAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = messaging.models.Event.objects.all()
    serializer_class = ResolveEventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, event_id):
        return self.queryset.filter(pk=event_id, users__pk=self.request.user.pk).first()

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        event = self.get_object(serializer.validated_data['event'])

        if not event:
            raise Http404

        response = serializer.resolve_event(event=event)

        return Response(response)
