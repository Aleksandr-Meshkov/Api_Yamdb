from ast import Pass
from api_yamdb.reviews.models import Categories

from reviews.models import Categories
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from .serializers import (CategoriesSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoriesVewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
