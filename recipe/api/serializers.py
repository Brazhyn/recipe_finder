from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser

from recipe.models import Ingredient, Recipe, Review


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
        ingredients = validated_data.pop("ingredients", None)
        liked_users = validated_data.pop("liked_users", None)
        recipe = Recipe.objects.create(author=author, **validated_data)

        if ingredients is not None and liked_users is not None:
            recipe.ingredients.set(ingredients)
            recipe.liked_users.set(liked_users)
        recipe.save()
        return recipe

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
        recipe = Recipe.objects.get(slug=slug)

        if Review.objects.filter(author=author, recipe=recipe).exists():
            raise ValidationError("You have already reviewed this movie!")

        if recipe.number_reviews == 0:
            recipe.avg_rating = validated_data["rating"]
        else:
            recipe.avg_rating = (recipe.avg_rating + validated_data["rating"]) / 2

        recipe.number_reviews += 1
        recipe.save()
        review = Review.objects.create(author=author, recipe=recipe, **validated_data)
        review.save()
        return review
