from django.conf.urls import url
from django.urls import include, path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework import routers
from rest_framework.authtoken import views as drf_views

from api.v1.auth_crm import views as auth_crm_api_v1_views
from api.v1.customers import views as customer_api_v1_views

router = routers.DefaultRouter()
router.register(r'customers', customer_api_v1_views.CustomerViewSet)
router.register(r'users', auth_crm_api_v1_views.UserViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="joseantoniohr87@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^token-auth/', drf_views.obtain_auth_token),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
