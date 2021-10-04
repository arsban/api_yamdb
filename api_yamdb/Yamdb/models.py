from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    bio = models.TextField()
    email = models.EmailField()

    class UserRole:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        choices = [
            (USER, 'user'),
            (ADMIN, 'admin'),
            (MODERATOR, 'moderator')
        ]
    
    role = models.CharField(
        max_length=25,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
