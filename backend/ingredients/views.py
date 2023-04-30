from .serializers import IngredientSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Ingredient
from rest_framework import filters


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    Вью сет для отображения ингредиентов
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
