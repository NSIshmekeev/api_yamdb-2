from django.shortcuts import get_object_or_404
from users.models import User
from rest_framework import permissions, viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from .serializers import SignupSerializer, TokenSerializer, UserSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from .permissions import IsItAdmin

from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title, Review
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly, IsStaffOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlePostSerializer,
    ReviewSerializer,
    CommentSerializer,
    TitleSerializer
)
from django.db.models import Avg

from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = [IsItAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ("=username",)
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        methods=["patch", "get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == "PATCH":
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get("email").lower()
    username = serializer.validated_data.get("username")
    user, _ = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Код подтверждения",
        f"Ваш код подтверждения: {confirmation_code}",
        settings.DEFAULT_EMAIL,
        [email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    confirmation_code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(
        {"confirmation_code": "Неверный код подтверждения!"},
        status=status.HTTP_400_BAD_REQUEST,
    )


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects \
        .prefetch_related("genre", "category") \
        .annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return TitlePostSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsStaffOrReadOnly,
    )

    def get_queryset(self):
        queryset = Review.objects.select_related('title').all()
        return queryset.filter(title=self.get_title())

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsStaffOrReadOnly,
    )

    def get_queryset(self):
        return self.get_review().comments.select_related('review__title').all()

    def get_review(self):
        return get_object_or_404(
            Review.objects.select_related('title'),
            title_id=self.kwargs.get("title_id"),
            pk=self.kwargs.get("review_id"),
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.get_review().id)
