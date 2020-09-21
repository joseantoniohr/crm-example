from rest_framework import serializers

from django.contrib.auth.models import User

from customers.models import Customer, CustomerLog


class CustomerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class CustomerSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)  # This field is autoincremental and its value isn't mutable.

    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'phone', 'email'
        ]


class FullCustomerSerializer(CustomerSerializer):

    created_by = CustomerUserSerializer(read_only=True)  # This field will be set automatically depending on action
    updated_by = CustomerUserSerializer(read_only=True)  # This field will be set automatically depending on action

    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'phone', 'email', 'photo',
            'country', 'postal_code', 'region', 'locality', 'address',
            'created_by', 'updated_by', 'created_at', 'updated_at'
        ]


class CustomerLogSerializer(serializers.ModelSerializer):

    user = CustomerUserSerializer()

    class Meta:
        model = CustomerLog
        fields = ['id', 'created_at', 'log_type', 'user', 'fields_changed']
