from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITransactionTestCase, force_authenticate

from api.v1.auth_crm import views as auth_crm_api_v1_views


class ApiV1UsersTest(APITransactionTestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.super_user = User.objects.create_superuser(username="super_user", password="TestPassword-20")
        self.not_super_user = User.objects.create_user(username="not_super_user", password="TestPassword-20")

    def test_can_not_create_a_user_with_an_existing_username(self):
        """ Usernames are unique in DB, so we have to control it in API """
        self._create_a_user(self.super_user, 'duplicated_username')
        self._create_a_user(self.super_user, 'duplicated_username', check_existing_username=True)

    def test_a_not_admin_user_can_not_access_to_users_endpoint(self):
        """ Not admin users aren't able to access to user endpoints """
        request = self.factory.get('/users/', format='json')
        view = auth_crm_api_v1_views.UserViewSet.as_view({'get': 'list'})
        force_authenticate(request, user=self.not_super_user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_not_revoke_admin_status_to_user(self):
        """ If a user is admin, its status mustn't revoke """
        new_user = self._create_a_user(self.super_user, 'new_username', is_superuser=True)
        self._update_a_user(self.super_user, user=new_user, is_superuser=True)

    def test_check_password_has_been_added_correctly(self):
        password = "TestPassword-20"
        new_user = self._create_a_user(self.super_user, 'new_username', password=password)

        # The function check_password checks if a raw password matches with hashed password in DB
        self.assertTrue(new_user.check_password("TestPassword-20"))

    def _create_a_user(self, action_user, username, password=None, is_superuser=True, check_existing_username=False):
        if not password:
            password = "TestPassword-20"

        request_data = {
            'username': username,
            'first_name': 'Name',
            'last_name': 'Surname',
            'email': 'mail@nomail.com',
            'password': password,
            'is_superuser': is_superuser
        }
        request = self.factory.post('/users/', request_data, format='json')
        view = auth_crm_api_v1_views.UserViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=action_user)
        response = view(request)

        if not check_existing_username:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            new_customer = User.objects.get(id=response.data.get('id'))
            return new_customer

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return None

    def _update_a_user(self, action_user, user, is_superuser=True, check_not_revoke_admin_status=False):
        request_data = {
            'first_name': 'New Name',
            'last_name': 'New Surname',
            'email': 'mail@nomail.com',
            'phone': '600 123 456',
            'is_superuser': is_superuser
        }

        request = self.factory.put('/users/{}/'.format(user.id), request_data, format='json')
        view = auth_crm_api_v1_views.UserViewSet.as_view({'put': 'update'})
        force_authenticate(request, user=action_user)
        response = view(request, pk=user.id)

        if check_not_revoke_admin_status:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            user.refresh_from_db()

        return user

    def _delete_a_customer(self, action_user, user):

        request = self.factory.delete('/users/{}/'.format(user.id), format='json')
        view = auth_crm_api_v1_views.UserViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request, user=action_user)
        response = view(request, pk=user.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
