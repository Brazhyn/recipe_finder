import django_filters

from recipe.models import Ingredient, Recipe, Review


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    caloric_min = django_filters.NumberFilter(
        field_name="caloric_content",
        lookup_expr="gte",
    )
    caloric_max = django_filters.NumberFilter(
        field_name="caloric_content",
        lookup_expr="lte",
    )
    category = django_filters.CharFilter(field_name="category", lookup_expr="iexact")

    class Meta:
        model = Ingredient
        fields = ["name", "caloric_min", "caloric_max", "category"]


class RecipeFilter(django_filters.FilterSet):
    ingredients = django_filters.CharFilter(
        field_name="ingredients__name",
        lookup_expr="iexact",
        method="filter_ingredients",
    )
    category = django_filters.CharFilter(field_name="category", lookup_expr="iexact")
    country = django_filters.CharFilter(field_name="country", lookup_expr="icontains")
    difficulty = django_filters.CharFilter(
        field_name="difficulty",
        lookup_expr="icontains",
    )

    class Meta:
        model = Recipe
        fields = ["ingredients", "category", "country", "difficulty"]

    def filter_ingredients(self, queryset, name, value):
        ingredients_list = value.split(",")

        for ingredient in ingredients_list:
            queryset = queryset.filter(ingredients__name__iexact=ingredient)

        return queryset


class ReviewFilter(django_filters.FilterSet):
    created_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
    )
    updated_after = django_filters.DateFilter(
        field_name="updated_at",
        lookup_expr="gte",
    )
    updated_before = django_filters.DateFilter(
        field_name="updated_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Review
        fields = ["created_after", "created_before", "updated_after", "updated_before"]
