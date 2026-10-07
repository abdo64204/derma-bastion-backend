from django.urls import path
from .views import ContactSubmitView

urlpatterns = [
    path('contact/', ContactSubmitView.as_view(), name='contact-submit'),
]
