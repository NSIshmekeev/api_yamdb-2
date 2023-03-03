from rest_framework import viewsets
from users.models import User


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()


def token():
    pass


def signup():
    pass
