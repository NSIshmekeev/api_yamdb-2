from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import get_token, signup, UserViewSet

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)

auth_patterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token'), ]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(auth_patterns))
]
