from django.urls import path
from .views import OrderCreateView, OrderDetailView, OrderTrackView, OrderUploadReceiptView

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/track/', OrderTrackView.as_view(), name='order-track'),
    path('orders/<str:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<str:pk>/receipt/', OrderUploadReceiptView.as_view(), name='order-upload-receipt'),
]
