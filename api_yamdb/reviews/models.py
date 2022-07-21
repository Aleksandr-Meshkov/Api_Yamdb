from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя', max_length=16, choices=ROLES, default='user'
    )
    email = models.EmailField('Почта пользователя', unique=True)
    confirmation_code = models.CharField(
        'Токен подтверждения', max_length=50, blank=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField('slug', blank=False, unique=True, max_length=50)

    def __str__(self):
        return self.text


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        'Дата публикации',
        blank=True,
        null=True,
        validators=[validate_year]
    )
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class AbstractModel(models.Model):
    text = models.TextField(verbose_name='Текст',)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['pub_date']

    def __str__(self):
        return self.text


class Review(AbstractModel):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        default=1,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )

    class Meta(AbstractModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(AbstractModel):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE, related_name='comments'

    )

    class Meta(AbstractModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
