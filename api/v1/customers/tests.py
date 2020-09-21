from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITransactionTestCase, force_authenticate

from api.v1.customers import views as customer_api_v1_views
from customers import choices as customer_choices
from customers.models import Customer


class ApiV1CustomersTest(APITransactionTestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.first_user = User.objects.create_user(username="first_user", password="TestPassword-20")
        self.second_user = User.objects.create_user(username="second_user", password="TestPassword-20")

    def test_created_and_updated_by_in_customer_creation(self):
        """ When a customer is created by an user, this is the value in created_by and updated_by """
        new_customer = self._create_a_customer(self.first_user)

        self.assertEqual(new_customer.created_by, self.first_user)
        self.assertEqual(new_customer.updated_by, self.first_user)

    def test_update_customer_by_different_user_that_creation(self):
        """ When a customer is updated, its updated_by fields will be the user of the request """
        customer = self._create_a_customer(self.first_user)
        updated_customer = self._update_a_customer(self.second_user, customer)

        self.assertNotEqual(updated_customer.created_by, updated_customer.updated_by)
        self.assertNotEqual(updated_customer.created_at, updated_customer.updated_at)
        self.assertEqual(updated_customer.updated_by, self.second_user)

    def test_delete_customer_is_a_soft_action(self):
        """ The customer aren't remove permanently from DB. We apply a soft delete """
        customer = self._create_a_customer(self.first_user)
        self._delete_a_customer(self.second_user, customer)

        # Customer won't appear with 'objects_not_deleted' model manager
        is_customer_deleted = False
        try:
            Customer.objects_not_deleted.get(id=customer.id)
        except Customer.DoesNotExist:
            is_customer_deleted = True
        self.assertTrue(is_customer_deleted)

        deleted_customer = Customer.objects.get(id=customer.id)
        self.assertTrue(deleted_customer.is_deleted)

    def test_can_not_access_to_customer_information_with_no_credentials(self):
        """ Anonymous user can't access to the customer endpoints """
        request = self.factory.get('/customers/', format='json')
        view = customer_api_v1_views.CustomerViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def _create_a_customer(self, user):
        request_data = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'email': 'mail@nomail.com',
            'phone': '600 123 456'
        }
        request = self.factory.post('/customers/', request_data, format='json')
        view = customer_api_v1_views.CustomerViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_customer = Customer.objects.get(id=response.data.get('id'))

        # Check that the creation log has been created
        self._check_logs_creation(customer=new_customer, new_log_type=customer_choices.LOG_CREATION_TYPE,
                                  old_number_of_logs=0)

        return new_customer

    def _update_a_customer(self, user, customer):
        old_number_of_logs, new_log = self._get_number_of_logs(customer=customer)

        request_data = {
            'first_name': 'New Name',
            'last_name': 'New Surname',
            'email': 'mail@nomail.com',
            'phone': '600 123 456'
        }

        request = self.factory.put('/customers/{}/'.format(customer.id), request_data, format='json')
        view = customer_api_v1_views.CustomerViewSet.as_view({'put': 'update'})
        force_authenticate(request, user=user)
        response = view(request, pk=customer.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        customer.refresh_from_db()

        # Check that the edition log has been created
        self._check_logs_creation(customer=customer, new_log_type=customer_choices.LOG_EDITION_TYPE,
                                  old_number_of_logs=old_number_of_logs)

        return customer

    def _delete_a_customer(self, user, customer):
        old_number_of_logs, new_log = self._get_number_of_logs(customer=customer)

        request = self.factory.delete('/customers/{}/'.format(customer.id), format='json')
        view = customer_api_v1_views.CustomerViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request, user=user)
        response = view(request, pk=customer.id)

        # Check that the edition log has been created
        self._check_logs_creation(customer=customer, new_log_type=customer_choices.LOG_DELETION_TYPE,
                                  old_number_of_logs=old_number_of_logs)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def _check_logs_creation(self, customer, new_log_type, old_number_of_logs):
        new_number_of_logs, new_log = self._get_number_of_logs(customer)
        self.assertEqual(old_number_of_logs + 1, new_number_of_logs)
        self.assertEqual(new_log.log_type, new_log_type)

    @staticmethod
    def _get_number_of_logs(customer):
        num_logs = customer.customerlog_set.count()
        new_log = customer.customerlog_set.first() if num_logs >= 1 else None

        return num_logs, new_log
