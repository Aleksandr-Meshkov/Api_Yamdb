import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, EmailSerializer, TokenSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly
from reviews.models import User


@api_view(['POST']) 
@permission_classes([AllowAny])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        if not User.objects.filter(email=email).exists():
            User.objects.create(
                username=username, email=email
            )
        confirmation_code = str(uuid.uuid4())
        send_mail('Токен подтверждения', confirmation_code,
                  settings.DEFAULT_FROM_EMAIL, [email])
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response("Отсутствует обязательное поле или оно некорректно", status=status.HTTP_400_BAD_REQUEST)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


    @action(methods=['get','patch'], detail=True, permission_classes=[IsAuthenticated])
    def me(self, request):       
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
             serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
