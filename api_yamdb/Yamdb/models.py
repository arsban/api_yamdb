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


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название категории')
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name='Уникальный идентификатор категории')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:20]


class Genre(models.Model):
    name = models.CharField(max_length=150, verbose_name='Жанр')
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name='Уникальный идентификатор жанра')

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:20]


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    year = models.PositiveSmallIntegerField()
    description = models.TextField(verbose_name='Описание произведения')
    genre = models.ManyToManyField(Genre, blank=True,
                                   related_name='genre_titles',
                                   verbose_name='Жанр', through='TitleGenre')
    category = models.ForeignKey(Category, blank=True, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='category_titles',
                                 verbose_name='Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def get_genres(self):
        return ",".join([str(gen) for gen in self.genre.all()])

    def __str__(self):
        return self.name[:20]


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        ordering = ['genre']
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'

    def __str__(self):
        return f'{self.genre} {self.title}'
