from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """
    Вью сет для вывода списка пользователей
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
