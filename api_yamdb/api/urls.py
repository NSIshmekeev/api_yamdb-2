from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import get_token, signup, UserViewSet
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

v1_router = DefaultRouter()
v1_router.register("users", UserViewSet)

v1_router.register("categories", CategoryViewSet, basename="categories")
v1_router.register("genres", GenreViewSet, basename="genres")
v1_router.register("titles", TitleViewSet, basename="titles")

v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)

v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)

auth_patterns = [
    path("auth/signup/", signup, name="signup"),
    path("auth/token/", get_token, name="token"),
]

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/", include(auth_patterns)),
]