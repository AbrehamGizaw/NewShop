from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from apps.core.views import Index, SearchItem
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('search/', SearchItem, name="search"),
    path('tinymce/', include('tinymce.urls')),
    path("accounts/", include("apps.accounts.urls"), ),
    path("notification/", include("apps.notifications.urls"), ),

    # APIS
    path('api/vendor/', include('apps.vendor.api.urls')),
    path('api/notifications/', include('apps.notifications.api.urls')),
    
    path('api/', include('apps.core.api.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    
]

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

