from rest_framework import serializers
from recipe.models import Ingredient, Recipe
from rest_framework.parsers import MultiPartParser, FormParser
        

class RecipeSerializer(serializers.ModelSerializer):
    parser_classes = (MultiPartParser, FormParser)
    
    class Meta:
        model = Recipe
        exclude = ['date_created','slug']
        

class IngredientSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(read_only=True, many=True)
    
    class Meta:
        model = Ingredient
        exclude = ['slug']