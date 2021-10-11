from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from Yamdb.models import User, Review, Comment

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
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
