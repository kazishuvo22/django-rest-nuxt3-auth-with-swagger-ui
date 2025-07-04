from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, LoginViewSet, RegisterViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),  # Your router URLs
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Add refresh token here
]
