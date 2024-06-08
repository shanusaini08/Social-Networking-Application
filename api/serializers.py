from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class SocialMediaUserSignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.
    """
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
            'blank': 'Email cannot be blank',
        }
    )
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 8 characters long.',
        },
        write_only=True,
        min_length=8
    )

    first_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'First Name is required.',
            'blank': 'First Name cannot be blank',
        }
    )

    last_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Last Name is required.',
            'blank': 'Last Name cannot be blank',
        }
    )

    username = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Username is required.',
            'blank': 'Username cannot be blank',
        }
    )

    class Meta:
        model = SocialMediaUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, data):
        """
        Validate email uniqueness and password match.
        """
        email = data.get('email')
        password = data.get('password')

        if SocialMediaUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email has already been registered.")

        return data

    def create(self, validated_data):
        """
        Create user with validated data.
        """
        email = validated_data.get('email')
        password = validated_data.get('password')
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = SocialMediaUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Validate email and password.
        """
        email = attrs.get('email').lower()  # Normalize the email to lowercase
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid email or password.')

            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')

            return user
        else:
            raise serializers.ValidationError('Email and password are required.')

class UserSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for user search.
    """
    class Meta:
        model = SocialMediaUser
        fields = ['id', 'username','first_name','last_name','email']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSearchSerializer()
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user']