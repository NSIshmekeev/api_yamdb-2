from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    CHOISES = [(USER, 'user'),
               (ADMIN, 'admin'),
               (MODERATOR, 'moderator')]

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True,)
    role = models.SlugField(choices=CHOISES, default=USER)

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff
