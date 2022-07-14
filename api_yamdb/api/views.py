from ast import Pass
from api_yamdb.reviews.models import Categories

from reviews.models import Categories, Titles
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CategoriesSerializer, TitlesSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('categories', 'genre', 'titles', 'year')

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)