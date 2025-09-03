import datetime

from django.utils import timezone

import pytest
from rest_framework.test import APIClient

from recipe.models import Ingredient, Recipe


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def users(django_user_model):
    users = [
        django_user_model.objects.create_user(
            email="michael2004@gmail.com",
            first_name="Michael",
            last_name="Row",
            phone="0987538747",
            password="qwerty123",
        ),
        django_user_model.objects.create_user(
            email="edward1995@gmail.com",
            first_name="Edward",
            last_name="Presley",
            phone="0962508147",
            password="qwerty123",
        ),
    ]
    users[0].date_joined = timezone.now() - datetime.timedelta(seconds=30)
    users[0].save()

    users[1].date_joined = timezone.now()
    users[1].save()
    users = sorted(users, key=lambda user: user.date_joined)
    return users


@pytest.fixture
def ingredients():
    ingredients = {
        "pizza": [
            Ingredient.objects.create(name="Flour", caloric_content=364),
            Ingredient.objects.create(name="Mozzarella", caloric_content=280),
            Ingredient.objects.create(name="Tomato", caloric_content=18),
            Ingredient.objects.create(name="Pepperoni", caloric_content=494),
            Ingredient.objects.create(name="Eggs", caloric_content=143),
            Ingredient.objects.create(name="Basil", caloric_content=100),
            Ingredient.objects.create(name="Olive Oil", caloric_content=884),
        ],
        "ratatouille": [
            Ingredient.objects.create(name="Aubergine", caloric_content=25),
            Ingredient.objects.create(name="Zucchini", caloric_content=17),
            Ingredient.objects.create(name="Tomatoes", caloric_content=18),
            Ingredient.objects.create(name="Bell pepper", caloric_content=31),
            Ingredient.objects.create(name="Onion", caloric_content=40),
            Ingredient.objects.create(name="Garlic", caloric_content=149),
            Ingredient.objects.create(name="Olive oil", caloric_content=884),
            Ingredient.objects.create(name="Thyme", caloric_content=101),
            Ingredient.objects.create(name="Basil", caloric_content=23),
        ],
    }
    return ingredients


@pytest.fixture
def recipes(users, ingredients):
    recipes = [
        Recipe.objects.create(
            name="Pizza Margarrita",
            category="lunch",
            description="some fantastic pizza",
            steps="1 step, 2 step, 3 step",
            total_cooking_time=60,
            difficulty="medium",
            country="Italy",
            avg_rating=3.2,
            author=users[0],
        ),
        Recipe.objects.create(
            name="Ratatouille",
            category="side_dish",
            description="some fantastic ratatouille",
            steps="1 step, 2 step, 3 step",
            total_cooking_time=90,
            difficulty="easy",
            country="France",
            avg_rating=4.0,
            author=users[0],
        ),
    ]

    recipes[0].ingredients.set(ingredients["pizza"])
    recipes[0].created_at = timezone.now()
    recipes[0].save()

    recipes[1].ingredients.set(ingredients["ratatouille"])
    recipes[1].created_at = timezone.now() - datetime.timedelta(seconds=30)
    recipes[1].save()
    recipes = sorted(recipes, key=lambda r: r.created_at, reverse=True)
    return recipes
