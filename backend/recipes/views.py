from .serializers import (
    RecipeListSerializer,
    RecipeSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .models import Recipe, FavoriteRecipe
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthorOrReadOnly
from rest_framework import filters
from .models import (ShoppingCartRecipe,
                     IngredientRecipe)


class RecipeViewSet(ModelViewSet):
    """
    ViewSet для работы с рецептами.
    Для анонимов разрешен только просмотр рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if not FavoriteRecipe.objects.filter(
                recipe=recipe, user=user).exists():
            return Response({'errors': 'Указанного рецепта нет в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        return self.delete_method_for_actions(
            request=request, pk=pk, model=FavoriteRecipe)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if not ShoppingCartRecipe.objects.filter(
                recipe=recipe, user=user).exists():
            return Response({'errors': 'Указанного рецепта нет в корзине'},
                            status=status.HTTP_400_BAD_REQUEST)
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCartRecipe)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('Handicraft', 'data/Handicraft.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('Handicraft', size=24)
        page.drawString(200, 800, 'Список покупок')
        page.setFont('Handicraft', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(75, height, (f'{i}. {name} - {data["amount"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response
