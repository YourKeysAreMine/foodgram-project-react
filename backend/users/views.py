from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins, viewsets

from .models import User, Follow
from .serializers import (CustomUserSerializer,
                          SubscriptionSerializer,
                          SubscriptionListSerializer)


class CustomUserViewSet(ModelViewSet):
    """
    Вью сет для вывода списка пользователей
    По ТЗ просматривать пользователей могут даже анонимы.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    Вью сет для добавления и удаления подписок.
    """
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.request.user.following.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author_id'] = self.kwargs.get('user_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            author=get_object_or_404(
                User,
                id=self.kwargs.get('user_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, user_id):
        get_object_or_404(User, id=user_id)
        if not Follow.objects.filter(
                user=request.user, author_id=user_id).exists():
            return Response({'errors': 'Вы не были подписаны на этого автора'},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Follow,
            user=request.user,
            author_id=user_id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowSubscriptionsViewSet(viewsets.ModelViewSet):
    """
    Вью-сет для отображения подписок.
    КОММЕНТАРИЙ ДЛЯ РЕВЬЮЕРА! Привет, ни в какую не получается сделать
    GET /api/users/subscriptions. Postman возвращает 404,
    "detail": "not found". Помоги пожалуйста, переписывал уже раз пять...
    """
    serializer_class = SubscriptionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
