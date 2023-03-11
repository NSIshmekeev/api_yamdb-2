from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    CHOISES = [(USER, "user"), (ADMIN, "admin"), (MODERATOR, "moderator")]

    username = models.SlugField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.SlugField(choices=CHOISES, default=USER)
    confirmation_code = models.SlugField(null=True, blank=True)

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
