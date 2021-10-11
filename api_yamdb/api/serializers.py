import re
from unicodedata import category

from yamdb.models import User, Category, Genre, Title, TitleGenre
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import datetime as dt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['email', 'username', 'bio', 'role']
        model = User
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'email']
        model = User
        extra_kwargs = {
            'email': {'required': True}
        }


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        extra_kwargs = {
            'name': {'required': False},
            'slug': {'validators': []},
        }

    def validate_slug(self, slug):
        if len(slug) > 50:
            return ValidationError("Slug должен быть не больше 50 символов")
        if re.match(r'^[-a-zA-Z0-9_]+$', slug):
            return ValidationError("Неверный формат Slug")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        extra_kwargs = {
            'name': {'required': False},
            'slug': {'validators': []},
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, read_only=False,
                                         queryset=Genre.objects.all(),
                                         slug_field='slug')
    category = serializers.SlugRelatedField(many=False, read_only=False,
                                            queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if not (1888 < value <= year):
            raise ValidationError('Указан некорректный год!')
        return value
