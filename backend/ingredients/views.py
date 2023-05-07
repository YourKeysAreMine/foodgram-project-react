from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models.query_utils import Q

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    Вью сет для отображения списка ингредиентов
    """
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get("name")
        if name is not None:
            qs_starts = queryset.filter(name__istartswith=name)
            qs_contains = queryset.filter(
                ~Q(name__istartswith=name) & Q(name__icontains=name)
            )
            queryset = list(qs_starts) + list(qs_contains)
        return queryset
