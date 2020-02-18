from django.urls import path

from .views import *  # noqa

app_name = 'core'
urlpatterns = [
    path('countries/', CountriesAPIView.as_view(), name='countries'),
]
