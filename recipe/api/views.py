from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.api.filters import RecipeFilter, ReviewFilter
from recipe.api.pagination import RecipePagination
from recipe.api.permissions import IsOwnerOrReadOnly
from recipe.api.serializers import RecipeSerializer, ReviewSerializer
from recipe.models import Recipe, Review


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all().order_by("-date_created")
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
    queryset = Recipe.objects.all()
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
        return Review.objects.filter(recipe__slug=slug)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


class LikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        user = request.user
        recipe = get_object_or_404(Recipe, slug=slug)

        if recipe.liked_users.filter(id=user.id).exists():
            recipe.liked_users.remove(user)
        else:
            recipe.liked_users.add(user)

        return Response(
            {"like_count": recipe.liked_users.count()}, status=status.HTTP_200_OK
        )
