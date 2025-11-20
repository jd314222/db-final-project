"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Register your viewsets here
# router.register(r'mobs', MobViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
