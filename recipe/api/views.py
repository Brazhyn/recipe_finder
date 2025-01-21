from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from recipe.models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'slug'


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'slug'
    



