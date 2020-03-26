from rest_framework import generics, permissions, parsers, viewsets, views
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

import core.models
import users.models
from ..serializers import *  # noqa


__all__ = (
    'ChangePasswordAPIView',
    'ChangeAvatarViewSet',
    'AddCarInfoAPIView',
    'AddCarAPIView',
    'EditCarAPIView',
    'EditUserAPIView',
    'ChangeNotificationViewSet',
    'ConnectDeviceAPIView',
)


class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context=dict(
                user=self.get_object()
            )
        )

        serializer.is_valid(raise_exception=True)
        response = serializer.change_password(
            user=self.get_object(),
            password=serializer.validated_data['new_password'],
        )

        return Response(response)


class ChangeAvatarViewSet(viewsets.ModelViewSet):
    queryset = users.models.User.objects.all()
    serializer_class = ChangeAvatarSerializer
    permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (parsers.MultiPartParser, )

    def get_object(self):
        return self.queryset.filter(pk=self.request.user.pk).first()


class AddCarInfoAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # noinspection PyUnusedLocal
    def get(self, request):
        return Response({
          'brands': core.models.Brand.as_choices(),
          'models': core.models.CarModel.as_choices_with_makes(),
        })


class AddCarAPIView(generics.CreateAPIView):
    queryset = users.models.Car.objects.all()
    serializer_class = AddEditCarSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EditCarAPIView(generics.UpdateAPIView):
    queryset = users.models.Car.objects.all()
    serializer_class = AddEditCarSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class EditUserAPIView(generics.UpdateAPIView):
    queryset = users.models.User.objects.all()
    serializer_class = EditUserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.queryset.get(pk=self.request.user.pk)


class ChangeNotificationViewSet(viewsets.ModelViewSet):
    queryset = users.models.Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class ConnectDeviceAPIView(GenericAPIView):
    queryset = users.models.User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangeDeviceSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.change_device(
            user=self.request.user,
            device=serializer.validated_data['device_id'],
        )

        return Response(response)
