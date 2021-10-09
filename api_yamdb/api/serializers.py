from Yamdb.models import User, Category, Genre, Title, TitleGenre
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        if not Category.objects.filter(name=category).exists():
            raise ValidationError('Укажите одну из существующих категорий!')
        title = Title.objects.create(
            **validated_data, category=Category.objects.filter(name=category)
        )
        for genre in genres:
            if not Genre.objects.filter(name=genre).exists():
                raise ValidationError(f'Жанра "{genre}" не существует!')
            TitleGenre.objects.create(genre=genre, title=title)
        return Title
