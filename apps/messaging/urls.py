from django.urls import path

from .views import *  # noqa

app_name = 'messaging'
urlpatterns = [
    path('send-message/', SendMessageAPIView.as_view(), name='send_message'),
]
