from django.contrib.auth.models import User

from rest_framework import filters, status, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.response import Response

from api.v1.base import DefaultPagination
from api.v1.auth_crm.permissions import IsSuperuserPermission
from api.v1.auth_crm.serializers import UserSerializer, UserEditionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    <h2>Enpoints for viewing and editing users.</h2>
    <p>When an user is created, a Token is created related with.</p>
    <ul>
        <li style="color: #D45151"><b>If you want to change the admin status, you have to set the field is_superuser equal to 'true'.</b></i>
        <li style="color: #D45151"><b>The username is unique, so you can't create a user with an existing username.</b></i>
        <li style="color: #D45151"><b>Username can be changed, but you can't use an existing username.</b></i>
    </ul>
    """
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = [IsSuperuserPermission]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def get_serializer_class(self):
        """
        The serializer depends on action, because in retrieve and list action won't show the password.
        However, in creation and edition will need this field
        :return:
        """
        if self.action in ['update']:
            return UserEditionSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # We use a soft deleted
        instance.is_active = False
        instance.save(update_fields=['is_active'])

        return Response(status=status.HTTP_204_NO_CONTENT)

