from rest_framework import serializers
from recipe.models import Ingredient, Recipe, Review
from rest_framework.parsers import MultiPartParser, FormParser
        

class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        exclude = ['slug']
        

class RecipeSerializer(serializers.ModelSerializer):
    parser_classes = (MultiPartParser, FormParser)
    author = serializers.StringRelatedField(read_only=True)
    # ingredients = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Recipe
        exclude = ['slug']
        
        
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ['recipe']
        

