from rest_framework import generics

import core.models
from .serializers import CountrySerializer


class CountriesAPIView(generics.ListAPIView):
    queryset = core.models.Country.objects.all()
    serializer_class = CountrySerializer
