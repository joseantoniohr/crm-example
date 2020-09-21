from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.base import DefaultPagination
from api.v1.customers.serializers import CustomerSerializer, FullCustomerSerializer, CustomerLogSerializer
from customers.models import Customer
from customers.log_manager import CustomerLogManager


class CustomerViewSet(viewsets.ModelViewSet):
    """
    <h2>Enpoints for viewing and editing customers.</h2>
    """
    queryset = Customer.objects_not_deleted.all()
    serializer_class = FullCustomerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone', 'email']

    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def get_serializer_class(self):
        """
        The serializer depends on action, because in list action a minimal information will be shown.
        :return:
        """
        if self.action in ['list']:
            return CustomerSerializer
        return FullCustomerSerializer

    def perform_create(self, serializer):
        """ This method is override to set created_by and updated_by in Customer and add creation log """
        # The current user is the creator and the last user that has updated it
        instance = serializer.save(created_by=self.request.user, updated_by=self.request.user)

        # Add log
        CustomerLogManager.add_creation_log(
            user=self.request.user, customer=instance, new_data=serializer.validated_data)

    def perform_update(self, serializer):
        """ This method is override to set updated_by in Customer and add edition log """
        # Get changed fields in instance
        updated_customer = self.get_object()
        changed_fields = Customer.get_changed_fields(new_data=serializer.validated_data, instance=updated_customer)

        # The current user is the last user that has updated it
        instance = serializer.save(updated_by=self.request.user)

        # Add log
        CustomerLogManager.add_edition_log(user=self.request.user, customer=instance, changed_fields=changed_fields)

    def destroy(self, request, *args, **kwargs):
        """ Destroy method is override to apply to add deletion log """
        instance = self.get_object()
        self.perform_destroy(instance)

        # Add log
        CustomerLogManager.add_deletion_log(user=request.user, customer=instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=True, url_path='logs')
    def customer_logs(self, request, pk):
        """
        Function that defines the endpoints to get the customer logs. Only GET method is allowed.
        :param request:
        :param pk: Customer ID
        :return: Paginated logs
        """
        customer = get_object_or_404(Customer.objects_not_deleted.all(), id=pk)

        queryset = customer.customerlog_set.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomerLogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CustomerLogSerializer(queryset, many=True)
        return Response(serializer.data)
