from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, send_confirmation_code

router_api_v1 = routers.DefaultRouter()
router_api_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', send_confirmation_code),
]
