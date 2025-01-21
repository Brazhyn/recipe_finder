from django.db import models
from django.utils.text import slugify


""" Generate unique slug for any model """
def create_slug_field(name, queryset):
    base_slug = slugify(name)
    unique_slug = base_slug
    num = 1
    while queryset.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{num}"
        num += 1
    return unique_slug

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    caloric_content = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, db_index=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug_field(self.name, Ingredient.objects.all())
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name}"
        

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('healthy', 'Healthy'),
        ('appetizer', 'Appetizers & Snacks'),
        ('salad', 'Salads'),
        ('soup', 'Soups'),
        ('bread', 'Bread'),
        ('side_dish', 'Side Dishes'),
        ('drink', 'Drinks'),
        ('dessert', 'desserts')
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    steps = models.TextField()
    total_cooking_time = models.PositiveIntegerField()
    difficulty = models.CharField(
        max_length=10,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
    )
    image = models.ImageField(upload_to='images_recipes/', blank=True, null=True)
    country = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, db_index=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug_field(self.name, Recipe.objects.all())
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name}"
        
    
    
    
    