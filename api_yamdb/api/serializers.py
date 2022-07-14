from rest_framework import serializers
from reviews.models import Categories, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = '__all__'