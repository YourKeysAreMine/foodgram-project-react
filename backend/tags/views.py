from .serializers import TagSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    """
    Вью сет для отображения тегов
    """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = TagSerializer