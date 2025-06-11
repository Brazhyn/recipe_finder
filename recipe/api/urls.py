from django.urls import include, path

from .views import LikeToggleAPIView, RecipeDetail, RecipeList, ReviewDetail, ReviewList

recipe_patterns = [
    path("", RecipeList.as_view(), name="recipe-list"),
    path("<slug:slug>/", RecipeDetail.as_view(), name="recipe-detail"),
    path("<slug:slug>/like-toggle/", LikeToggleAPIView.as_view(), name="like-toggle"),
    path("<slug:slug>/reviews/", ReviewList.as_view(), name="review-list"),
    path("<slug:slug>/reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
]

urlpatterns = [
    path("recipes/", include(recipe_patterns)),
]
