from django.urls import include, path

from api.views import CategoriesViewSet, TitlesViewSet
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet)
v1_router.register('titles', CategoriesViewSet)
urlpatterns = [
    path('v1/', include(v1_router.urls))
]