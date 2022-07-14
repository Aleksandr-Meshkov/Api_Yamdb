from django.urls import include, path

from api.views import CategiriesViewSet
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('categories', CategiriesViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls))
]