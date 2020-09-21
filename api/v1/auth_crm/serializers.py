from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.validators import UniqueValidator

from api.v1.auth_crm import validators as api_v1_auth_crm_validators


class UserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)  # This field is autoincremental and its value isn't mutable.
    password = serializers.CharField(write_only=True, max_length=128, required=False)

    class Meta:
        """
        We don't declare the 'password' field because we don't want that appears in responses
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'is_superuser', 'password']

    def __init__(self, instance=None, data=empty, **kwargs):
        self.password = data.get('password', None) if isinstance(data, dict) else None  # Get password from initial data
        super(UserSerializer, self).__init__(instance, data, **kwargs)

    def save(self, **kwargs):
        """
        We override this method to establish the password passed in request
        :param kwargs:
        :return:
        """
        self.instance = super(UserSerializer, self).save(**kwargs)
        if self.password:  # Save password
            self.instance.set_password(self.password)
            self.instance.save()

        return self.instance

    def validate_password(self, value):
        """
        This is generic function to validate all serializer fields.
        Here we validate the password, We check in 'validate' function because this field is not declared in Meta class.
        :param value:
        :return:
        """
        if self.password:
            password_validators = password_validation.get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
            password_validation.validate_password(self.password, password_validators=password_validators)

        return value

    def validate_is_superuser(self, value):
        """
        This function is called automatically by serializer. For declared field you override the validator
        whit format -> def validate_'field_name'(self, value)
        :param value:
        :return:
        """
        if self.instance and self.instance.is_superuser and not value:
            raise serializers.ValidationError(detail="You can revoke the admin status to this user")
        return value


class UserEditionSerializer(UserSerializer):
    """
    We declare a new serializer for PUT method, because we don't want that username is required for that method
    """
    username = serializers.CharField(
        required=False, max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())])

    @staticmethod
    def validate_username(value):
        validator = api_v1_auth_crm_validators.UsernameUnicodeValidator()
        validator.__call__(value)
        return value
