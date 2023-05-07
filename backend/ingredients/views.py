from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    Вью сет для отображения списка ингредиентов
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
