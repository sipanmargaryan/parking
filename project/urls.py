from rest_framework_swagger.views import get_swagger_view

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

schema_view = get_swagger_view(title=f'{settings.CLIENT_DOMAIN} API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(f'api/v{settings.API_VERSION}/public/', include('core.urls', namespace='core')),
    path(f'api/v{settings.API_VERSION}/accounts/', include('users.urls', namespace='users')),
    path(f'api/v{settings.API_VERSION}/messaging/', include('messaging.urls', namespace='messaging')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += [
        path('api-docs/', schema_view)
    ]
