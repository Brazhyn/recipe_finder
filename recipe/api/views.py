from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipe.api.filters import IngredientFilter, RecipeFilter, ReviewFilter
from recipe.api.pagination import RecipePagination
from recipe.api.permissions import IsOwnerOrReadOnly
from recipe.api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    ReviewSerializer,
)
from recipe.models import Ingredient, Recipe, Review
from services.recipe.daily_recipes_service import DailyRecipesService
from services.recipe.recipe_service import LikeService
from utils.location import get_user_ip, get_user_location_by_ip


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = IngredientFilter
    search_fields = ["name"]
    ordering_fields = ["caloric_content"]


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.select_related("author").order_by("-created_at")
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = RecipeFilter
    search_fields = ["name"]
    ordering_fields = ["avg_rating"]
    pagination_class = RecipePagination


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.select_related("author").defer("slug")
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "slug"


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_queryset(self):
        slug = self.kwargs["slug"]
        return (
            Review.objects.filter(recipe__slug=slug)
            .select_related("author")
            .defer("recipe")
        )


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all().defer("recipe")
    permission_classes = [IsOwnerOrReadOnly]


class LikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        user = request.user
        recipe = get_object_or_404(Recipe, slug=slug)

        liked = LikeService.toggle_like(user=user, recipe=recipe)

        return Response(
            {"liked": liked, "like_count": recipe.liked_users.count()},
            status=status.HTTP_200_OK,
        )


class DailyRecipesAPIView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        ip = get_user_ip(self.request)
        location = get_user_location_by_ip(ip)
        daily_recipes_service = DailyRecipesService(location)
        return daily_recipes_service.get_daily_recipes()
