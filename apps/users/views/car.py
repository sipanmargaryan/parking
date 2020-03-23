from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

import users.models
from users.utils import random_with_n_digits
from ..serializers import CarSerializer


__all__ = (
    'CarAPIView',
    'DeleteCarAPIView',
    'CheckCarAPIView',
)


class CarAPIView(generics.ListAPIView):
    queryset = users.models.Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, deleted=False).select_related('car_model__make', 'car_model')


class DeleteCarAPIView(generics.DestroyAPIView):
    queryset = users.models.Car.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.car_number = f'{instance.car_number}_{random_with_n_digits(6)}'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckCarAPIView(generics.RetrieveAPIView):
    queryset = users.models.Car.objects.all()
    lookup_field = 'car_number'

    def get_queryset(self):
        return self.queryset.filter(deleted=False)

    def retrieve(self, request, *args, **kwargs):
        response = dict(valid=True)
        try:
            self.get_object()
        except Exception as e:
            response['valid'] = False

        return Response(response)

