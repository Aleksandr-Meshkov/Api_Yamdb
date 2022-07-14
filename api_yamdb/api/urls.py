from django.urls import include, path

from api.views import CategoriesViewSet, TitlesViewSet, GenresViewSet
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet)
v1_router.register('titles', TitlesViewSet)
v1_router.register('genres', GenresViewSet)
urlpatterns = [
    path('v1/', include(v1_router.urls))
]