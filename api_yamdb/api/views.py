import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          EmailSerializer, GenresSerializer, ReviewSerializer,
                          TitlesGetSerializer, TitlesSerializer,
                          TokenSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    confirmation_code = str(uuid.uuid4())
    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            confirmation_code=confirmation_code
        )
    except IntegrityError:
        return Response(
            'Неверные данные ошибка', status=status.HTTP_400_BAD_REQUEST
        )
    send_mail(
        'Сonfirmation_code',
        f'Ваш код подтверждения {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL, [email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token_for_user(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        tokens = {
            'access': str(refresh.access_token)
        }
        return Response(tokens, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]
    base_model = None
    id_name = None
    record_name = None

    def get_base_record(self):
        return get_object_or_404(
            self.base_model, pk=self.kwargs.get(self.id_name)
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            **{self.record_name: get_object_or_404(
                self.base_model, pk=self.kwargs.get(self.id_name)
            )
            }
        )


class ReviewViewSet(RecordViewSet):
    serializer_class = ReviewSerializer
    base_model = Title
    id_name = "title_id"
    record_name = "title"

    def get_queryset(self):
        return self.get_base_record().reviews.all()


class CommentViewSet(RecordViewSet):
    serializer_class = CommentSerializer
    base_model = Review
    id_name = "review_id"
    record_name = "review"

    def get_queryset(self):
        return self.get_base_record().comments.all()


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitleFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesGetSerializer
        return TitlesSerializer


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
