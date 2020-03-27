from django.contrib import admin

import messaging.models

admin.site.register(messaging.models.MessageTemplate)
admin.site.register(messaging.models.Event)
