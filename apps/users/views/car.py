from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from django.db.models import F, Func, Value

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

    def get_object(self):
        response = dict(valid=True)
        car_number = self.kwargs[self.lookup_field].replace(' ', '')
        try:
            self.queryset.annotate(car_number_s=Func(F('car_number'), Value(' '), Value(''), function='REPLACE'))\
                .get(car_number_s__icontains=car_number)
        except users.models.Car.DoesNotExist:
            response['valid'] = False

        return response

    def retrieve(self, request, *args, **kwargs):
        return Response(self.get_object())

