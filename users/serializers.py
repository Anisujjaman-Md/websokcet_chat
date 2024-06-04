from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=email,
            password=validated_data['password']
        )
        return user

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        return {
            'username': instance.username,
            'email': instance.email,
            'refresh': str(token),
            'access': str(token.access_token),
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Extract user from validated data
        user = self.user

        data.update({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
            }
        })

        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password']
