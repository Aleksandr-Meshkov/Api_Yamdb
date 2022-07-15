from django.http import HttpResponse
from reviews.models import Categories, Titles, Genres
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CategoriesSerializer, TitlesSerializer, GenresSerializer, TitlesGetSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.contrib.auth import get_user_model
User = get_user_model()


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    # def perform_create(self, serializer):
        # serializer.save(self.request.user.is_superuser)
    #     serializer.save(user=self.request.user)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('categories', 'genres', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesGetSerializer
        return TitlesSerializer


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    # def perform_create(self, serializer):
    #     serializer.save(admin=self.request.user)


def load(request):
    # with open('static/data/category.csv', encoding='utf8') as f:
    #     f.readline()
    #     for line in f:
    #         id,name,slug=line.strip().split(',')
    #         category=Categories(name=name, slug=slug)
    #         category.save()
    # with open('static/data/titles.csv', encoding='utf8') as f:
    #     f.readline()
    #     for line in f:
    #         id,title_id,genre_id=line.strip().split(',')
    #         title=Titles(name=name, year=year)
    #         title.save()
    with open('static/data/titles.csv', encoding='utf8') as f:
        f.readline()
        for line in f:
            id,name,year,category=line.strip().split(',')
            title=Titles(name=name, year=year, category=categories)
            title.save()
    return HttpResponse('ok')