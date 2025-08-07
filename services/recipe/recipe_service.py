from rest_framework.exceptions import ValidationError

from account.models import User
from recipe.models import Recipe, Review


class RecipeService:
    @staticmethod
    def create_recipe(author: User, validated_data: dict) -> Recipe:
        ingredients = validated_data.pop("ingredients", None)
        liked_users = validated_data.pop("liked_users", None)
        recipe = Recipe.objects.create(author=author, **validated_data)

        if ingredients is not None and liked_users is not None:
            recipe.ingredients.set(ingredients)
            recipe.liked_users.set(liked_users)
        recipe.save()

        return recipe


class ReviewService:
    @staticmethod
    def create_review(author: User, slug: str, validated_data: dict) -> Review:
        recipe = Recipe.objects.get(slug=slug)

        if Review.objects.filter(author=author, recipe=recipe).exists():
            raise ValidationError("You have already reviewed this movie!")

        if recipe.number_reviews == 0:
            recipe.avg_rating = validated_data["rating"]
        else:
            recipe.avg_rating = (recipe.avg_rating + validated_data["rating"]) / 2

        recipe.number_reviews += 1
        recipe.save()
        return Review.objects.create(author=author, recipe=recipe, **validated_data)


class LikeService:
    @staticmethod
    def toggle_like(user: User, recipe: Recipe) -> bool:
        if recipe.liked_users.filter(id=user.id).exists():
            recipe.liked_users.remove(user)
            return False
        else:
            recipe.liked_users.add(user)
            return True
