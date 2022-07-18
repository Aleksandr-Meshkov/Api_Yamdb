from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from reviews.models import User, Comment, Review


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
        if value == 'me':
            raise serializers.ValidationError(
                "У пользователя не может быть имени me"
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
    
    
class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Пользователь может оставлять отзыв на каждое произведение'
                    'не более одного раза'
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
