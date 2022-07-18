from django.urls import include, path

from rest_framework import routers

from .views import UserViewSet, send_confirmation_code, get_token_for_user

router_api_v1 = routers.DefaultRouter()
router_api_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', get_token_for_user),
]
