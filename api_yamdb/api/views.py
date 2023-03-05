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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsItAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=username',)

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            username=email, email=email
        )
    user = User.objects.filter(email=email).first()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения от сервиса Yamdb',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_EMAIL,
        [email]
    )
    return Response(
        {'result': 'Код подтверждения отправлен на вашу почту. Проверьте!'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный указан код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )
