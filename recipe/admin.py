from django.contrib import admin

from .models import Ingredient, Recipe, Review


class IngredientAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["id", "name", "category"]
    search_fields = ["name"]
    list_filter = []


class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ("ingredients",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author", "rating", "recipe"]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Review, ReviewAdmin)
