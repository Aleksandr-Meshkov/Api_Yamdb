from rest_framework import serializers
from reviews.models import Categories, Titles, Genres
from rest_framework.relations import SlugRelatedField


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    categories = SlugRelatedField(slug_field='name', read_only=True)
    genres = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')