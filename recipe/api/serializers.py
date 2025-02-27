from rest_framework import serializers
from rest_framework.parsers import FormParser, MultiPartParser

from recipe.models import Ingredient, Recipe, Review


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        exclude = ["slug"]


class RecipeSerializer(serializers.ModelSerializer):
    parser_classes = (MultiPartParser, FormParser)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ["slug"]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ["recipe"]
