from djoser.views import UserViewSet
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow, User
from .serializers import (CustomUserSerializer, SubscriptionListSerializer,
                          SubscriptionSerializer)


class CustomUserViewSet(UserViewSet):
    """
    Вью сет для вывода списка пользователей
    По ТЗ просматривать пользователей могут даже анонимы.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


class SubscriptionView(APIView):
    """
    Вью сет для добавления и удаления подписок.
    """
    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = SubscriptionSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if not Follow.objects.filter(user=request.user,
                                     author=author).exists():
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.get(user=request.user.id,
                           author=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowSubscriptionsViewSet(mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = SubscriptionListSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
