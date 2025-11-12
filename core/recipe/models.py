from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


def create_slug_field(name, queryset):
    """Generate unique slug for any model"""
    base_slug = slugify(name)
    unique_slug = base_slug
    num = 1
    while queryset.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{num}"
        num += 1
    return unique_slug


class Ingredient(models.Model):
    CATEGORY_CHOICES = [
        ("dairy", "Dairy Products"),
        ("meat", "Meat"),
        ("fish", "Fish"),
        ("seafood", "Seafood"),
        ("vegetables", "Vegetables"),
        ("fruits", "Fruits"),
        ("mushrooms", "Mushrooms"),
        ("grains", "Grains"),
        ("legumes", "Legumes"),
        ("flour", "Flour"),
        ("spices_sauces", "Spices and Sauces"),
        ("sweets", "Sweets"),
        ("beverages", "Beverages"),
        ("oils", "Oils"),
        ("nuts", "Nuts"),
        ("herbs", "Herbs"),
        ("condiments", "Condiments"),
        ("bakery", "Bakery"),
    ]

    name = models.CharField(max_length=50)
    caloric_content = models.PositiveIntegerField(default=0)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="vegetables",
    )
    slug = models.SlugField(unique=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug_field(self.name, Ingredient.objects.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.category}"


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("healthy", "Healthy"),
        ("appetizer", "Appetizers & Snacks"),
        ("salad", "Salads"),
        ("soup", "Soups"),
        ("bread", "Bread"),
        ("side_dish", "Side Dishes"),
        ("drink", "Drinks"),
        ("dessert", "desserts"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    steps = models.TextField()
    total_cooking_time = models.PositiveIntegerField()
    difficulty = models.CharField(
        max_length=10,
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
    )
    image = models.ImageField(upload_to="images_recipes/", blank=True, null=True)
    country = models.CharField(max_length=100)
    avg_rating = models.FloatField(default=0, blank=True, null=True)
    number_reviews = models.IntegerField(default=0, blank=True, null=True)
    liked_users = models.ManyToManyField(
        get_user_model(),
        related_name="liked_recipes",
        blank=True,
    )
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="recipes",
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, db_index=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug_field(self.name, Recipe.objects.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Review(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
    )
    description = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
