from django.urls import path

from services.health_check.rest import HelloView

urlpatterns = [
    path('health-check', HelloView.as_view(), name='health-check'),
]
