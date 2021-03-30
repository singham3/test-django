from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class AuthUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = "__all__"

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(AuthUserSerializer, self).create(validated_data)
