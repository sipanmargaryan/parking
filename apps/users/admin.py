from django.contrib import admin

import users.models

admin.site.register(users.models.User)
admin.site.register(users.models.Car)
