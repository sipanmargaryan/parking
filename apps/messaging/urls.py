from django.urls import path

from .views import *  # noqa

app_name = 'messaging'
urlpatterns = [
    path('send-message/', SendMessageAPIView.as_view(), name='send_message'),
    path('resolve/', ResolveEventAPIView.as_view(), name='resolve_event'),
]
