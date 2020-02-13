from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.utils import get_file_path
import users.models

__all__ = (
    'Event',
    'Message',
    'MessageTemplate',
)


class MessageTemplate(models.Model):
    message_text = models.TextField()

    class Meta:
        verbose_name_plural = 'message templates'


class Event(models.Model):

    resolved = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_file_path, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    car = models.ForeignKey(users.models.Car, on_delete=models.CASCADE)
    users = models.ManyToManyField(get_user_model())

    def __str__(self):
        return f'{self.car} - Chat'

    def get_absolute_url(self):
        return reverse('messaging:inbox_detail', kwargs={'pk': self.pk})

    @property
    def chat_url(self):
        if not self.pk:
            raise ValueError('pk is None')

        return f'/chat/{self.pk}/'


class Message(models.Model):

    message = models.TextField()
    unread = models.BooleanField(default=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.message
