import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        read_only_field = ('role',)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Такой имеил уже есть в базе')
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Такое имя уже есть в базе')
        ]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "У пользователя не может быть имени me"
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Пользователь может оставлять отзыв на каждое произведение'
                'не более одного раза.'
            )
        return data

    def validate_score(self, value):
        MinValueValidator = 1
        MaxValueValidator = 10
        if not MinValueValidator <= value <= MaxValueValidator:
            raise serializers.ValidationError(
                'Оценкой может быть целое число в диапазоне от 1 до 10.'
            )
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genre.objects.all())

    def validate_year(self, value):
        now_year = dt.date.today()
        if value > now_year.year:
            raise serializers.ValidationError('Некорректный год')
        return value

    class Meta:
        model = Title
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False, required=True)
    genre = GenresSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
