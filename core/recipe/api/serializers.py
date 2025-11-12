from rest_framework import serializers
from rest_framework.parsers import FormParser, MultiPartParser

from core.recipe.models import Ingredient, Recipe, Review
from core.services.recipe.recipe_service import RecipeService, ReviewService


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    parser_classes = (MultiPartParser, FormParser)
    author = serializers.EmailField(
        source="author.email",
        read_only=True,
    )
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = "__all__"

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
    author = serializers.EmailField(
        source="author.email",
        read_only=True,
    )

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
