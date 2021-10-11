from Yamdb.models import User, Category, Genre, Title, TitleGenre
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
        fields = ['email']
        model = User
        extra_kwargs = {
            'email': {'required': True}
        }


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        extra_kwargs = {
            'name': {'required': False},
            'slug': {'validators': []},
        }


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
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if not (1888 < value <= year):
            raise ValidationError('Указан некорректный год!')
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')['slug']
        if not Category.objects.filter(slug=category).exists():
            raise ValidationError(f'Укажите одну из существующих категорий!')
        category_object = Category.objects.filter(slug=category).get()
        title = Title.objects.create(
            **validated_data, category=category_object
        )
        for genre in genres:
            if not Genre.objects.filter(slug=genre['slug']).exists():
                raise ValidationError(f'Жанра "{genre}" не существует!')
            genre_object = Genre.objects.filter(slug=genre['slug']).get()
            TitleGenre.objects.create(genre=genre_object, title=title)
        return Title
