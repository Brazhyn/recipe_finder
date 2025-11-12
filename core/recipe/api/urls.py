from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    DailyRecipesAPIView,
    IngredientViewSet,
    LikeToggleAPIView,
    RecipeDetail,
    RecipeList,
    ReviewDetail,
    ReviewList,
)

router = DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredient")

recipe_patterns = [
    path("", RecipeList.as_view(), name="recipe-list"),
    path("daily-recipes/", DailyRecipesAPIView.as_view(), name="daily-recipes"),
    path("<slug:slug>/", RecipeDetail.as_view(), name="recipe-detail"),
    path("<slug:slug>/like-toggle/", LikeToggleAPIView.as_view(), name="like-toggle"),
    path("<slug:slug>/reviews/", ReviewList.as_view(), name="review-list"),
    path("<slug:slug>/reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
]

urlpatterns = [
    path("recipes/", include(recipe_patterns)),
    path("", include(router.urls)),
]
