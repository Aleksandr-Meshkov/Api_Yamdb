from rest_framework import serializers
from reviews.models import Categories, Titles, Genres
from rest_framework.relations import SlugRelatedField
import datetime as dt


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    categories = SlugRelatedField(slug_field='slug', queryset=Categories.objects.all())
    genres = SlugRelatedField(slug_field='slug', many=True, queryset=Genres.objects.all())

    class Meta:
        model = Titles
        fields = '__all__'

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год')
        return value


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):
    """Основной метод получения информации."""

    categories = CategoriesSerializer(many=False, required=True)
    genres = GenresSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genres',
            'categories'
        )
        model = Titles
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genres',
            'categories'
        )

