from django.contrib import admin

import core.models

admin.site.register(core.models.Country)
admin.site.register(core.models.Brand)
admin.site.register(core.models.CarModel)
admin.site.register(core.models.Color)
