from django.contrib import admin
from .models import Ingredient, Recipe, Review

class IngredientAdmin(admin.ModelAdmin):
    ordering = ['name']

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe)
admin.site.register(Review)


