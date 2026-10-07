"""
URL configuration for derma_backend project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import JsonResponse

# Custom Admin Site Branding
admin.site.site_header = "Derma Bastion Administration"
admin.site.site_title = "Derma Bastion Admin Portal"
admin.site.index_title = "Store Management & Fulfillment Dashboard"


def root_health_view(request):
    return JsonResponse({
        "status": "online",
        "service": "Derma Bastion API",
        "version": "1.0.0",
        "admin": "/admin/",
        "endpoints": {
            "products": "/api/products/",
            "orders": "/api/orders/",
            "store_config": "/api/store-config/",
            "contact": "/api/contact/",
        }
    })


urlpatterns = [
    path('', root_health_view, name='api-root-health'),
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('store_settings.urls')),
    path('api/', include('contact.urls')),
]

# Static & Media URL handling
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Media serving fallback for production (in case Web tab static mapping is not configured)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
