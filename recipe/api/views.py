from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.api.filters import RecipeFilter, ReviewFilter
from recipe.api.pagination import RecipePagination
from recipe.api.permissions import IsOwnerOrReadOnly
from recipe.api.serializers import RecipeSerializer, ReviewSerializer
from recipe.models import Like, Recipe, Review


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
        try:
            recipe = Recipe.objects.get(slug=slug)
        except Recipe.DoesNotExist:
            return Response(
                {"detail": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND
            )

        like_obj = Like.objects.filter(user=user, recipe=recipe).first()
        if like_obj:
            like_obj.delete()
            recipe.like_count = recipe.like_count - 1 if recipe.like_count > 0 else 0
            recipe.save(update_fields=["like_count"])
            return Response({"detail": "You removed your like"})
        else:
            Like.objects.create(user=user, recipe=recipe)
            recipe.like_count += 1
            recipe.save(update_fields=["like_count"])
            return Response({"liked": True, "like_count": recipe.like_count})
