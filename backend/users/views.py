from djoser.views import UserViewSet
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

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


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    Вью сет для добавления и удаления подписок.
    """
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)

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
    GET /api/users/subscriptions. Postman возвращает 404, без дебаг сообщений,
    просто "detail": "not found". Помоги пожалуйста, переписывал уже раз пять.
    Создавал два треда, именно по этому вопросу никто не помог...
    Причём, что интересно, при подписке по эндпоинту
    POST /api/users/user_id/sibscribe. Postman возвращает ответ согласно ТЗ.
    То есть ошибки во вью-сете быть не может, так как вью сет выше для ПОСТ
    запросов для добавления подписок я писал максимально идентичным.
    Я даже через APIView пробовал, ничего не выходит...
    """
    serializer_class = SubscriptionListSerializer

    def get_queryset(self):
        return User.objects.filter(follower__user=self.request.user)
