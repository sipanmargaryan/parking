from rest_framework import generics, permissions, parsers, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.http import Http404

import users.models
from ..serializers import *  # noqa


__all__ = (
    'ChangePasswordAPIView',
    'ChangeAvatarViewSet',
    'AddCarAPIView',
    'EditCarAPIView',
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
