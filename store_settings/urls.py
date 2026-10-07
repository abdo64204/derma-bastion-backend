from django.urls import path
from .views import StoreConfigView

urlpatterns = [
    path('store-config/', StoreConfigView.as_view(), name='store-config'),
]
