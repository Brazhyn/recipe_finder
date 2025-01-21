from django.urls import path, include
from .views import RecipeList, RecipeDetail


recipe_patterns = [
    path('', RecipeList.as_view(), name='recipe-list'),
    path('<slug:slug>/', RecipeDetail.as_view(), name='recipe-detail'),
]

urlpatterns = [
    path('recipes/', include(recipe_patterns)),
]