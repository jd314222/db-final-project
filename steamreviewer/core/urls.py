from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'games', views.GamesViewSet, basename='games')
router.register(r'reviews', views.ReviewsViewSet, basename='reviews')
router.register(r'genres', views.GenresViewSet, basename='genres')
router.register(r'developers', views.DevelopersViewSet, basename='developers')
router.register(r'users', views.UsersViewSet, basename='users')
router.register(r'user-specs', views.UserSpecsViewSet, basename='user-specs')
router.register(r'wishlist', views.UserWishListViewSet, basename='wishlist')
router.register(r'analytics', views.ReviewAnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]
