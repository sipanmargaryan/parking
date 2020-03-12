from rest_framework import generics, permissions

import users.models

from ..serializers import CarSerializer


class CarAPIView(generics.ListAPIView):
    queryset = users.models.Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related('car_model__make', 'car_model')
