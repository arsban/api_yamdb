from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 
                  'bio',  'role']
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
