import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
    


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    email = models.EmailField(
        'Email',
        unique=True,
        max_length=254
    )
    username = models.CharField(
        'Никнеим',
        max_length=150,
        unique=True,
        help_text=(
            'Обязательное поле, только цифры, буквы или @/./+/-/_.'
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с таким никнеимом уже существует.',
        },
        blank=True,
        null=True,
    )
    bio = models.TextField(
        'О себе',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Статус',
        max_length=16,
        choices=CHOICES,
        default=CHOICES[0],
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True,
        default=uuid.uuid4
    )

    @property
    def is_user(self):
        return self.role == self.USER or self.is_admin or self.is_moderator

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_admin
    

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff is True
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'