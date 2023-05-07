from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    """
    Вью сет для отображения списка тегов
    """
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Tag.objects.all()
