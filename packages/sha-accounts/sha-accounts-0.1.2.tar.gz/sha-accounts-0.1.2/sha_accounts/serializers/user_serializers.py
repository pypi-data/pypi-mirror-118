from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from djrest_wrapper.exceptions.apis.exceptions import DoesNotExistsExp
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from ..models.user_models import User
from .profile_serializers import ProfileSerializer


class UserSignUpRequest(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserSignUpResponse(WritableNestedModelSerializer):
    profile = ProfileSerializer()
    access_token = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'is_active', 'is_superuser', 'profile', 'access_token']


class UserSignInRequest(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def login(self):
        username = self.validated_data.get('username')
        password = self.validated_data.get('password')
        try:
            user = self.Meta.model.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                raise DoesNotExistsExp(f'Invalid Credentials')
        except ObjectDoesNotExist as e:
            raise DoesNotExistsExp(f'Invalid Credentials')


class UserSignInResponse(UserSignUpResponse):
    class Meta(UserSignUpResponse.Meta):
        pass
