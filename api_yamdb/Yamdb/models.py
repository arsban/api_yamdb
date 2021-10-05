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
            'unique': 'Пользователь с таким никнетмом уже существует.',
        },
        blank=True,
        null=True,
    )
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
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
    password = models.CharField('Пароль', max_length=25)


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'
    

    @property
    def is_user(self):
        return self.role == Role.USER or self.is_admin or self.is_moderator

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR or self.is_admin
    

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_staff is True
