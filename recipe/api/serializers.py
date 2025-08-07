from rest_framework import serializers
from rest_framework.parsers import FormParser, MultiPartParser

from recipe.models import Ingredient, Recipe, Review
from services.recipe.recipe_service import RecipeService, ReviewService


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = ["slug"]


class RecipeSerializer(serializers.ModelSerializer):
    parser_classes = (MultiPartParser, FormParser)
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ["slug"]

    def create(self, validated_data):
        author = self.context["request"].user
        return RecipeService.create_recipe(author=author, validated_data=validated_data)

    def get_likes_count(self, obj):
        return obj.liked_users.count()

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.liked_recipes.filter(id=obj.id).exists()
        return False


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ["recipe"]

    def create(self, validated_data):
        slug = self.context["view"].kwargs["slug"]
        author = self.context["request"].user

        return ReviewService.create_review(
            author=author,
            slug=slug,
            validated_data=validated_data,
        )
