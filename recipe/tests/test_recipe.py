import pytest
from django.urls import reverse
from rest_framework import status

from recipe.models import Ingredient, Recipe


@pytest.mark.django_db
def test_recipe_empty_list(client):
    recipe_url = reverse("recipe-list")
    response = client.get(recipe_url)
    data = response.data["results"]

    assert response.status_code == status.HTTP_200_OK
    assert data == []


@pytest.mark.django_db
def test_get_recipe_list(client, recipes):
    recipe_url = reverse("recipe-list")
    response = client.get(recipe_url)
    data = response.data["results"]

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == len(recipes)
    assert data[0]["id"] == recipes[0].id
    assert data[0]["name"] == recipes[0].name
    assert data[0]["category"] == recipes[0].category
    assert data[0]["author"] == recipes[0].author.email


@pytest.mark.parametrize(
    "search_term, expected_recipe_name, unexpected_recipe_name",
    [
        ("pizza", "Pizza Margarrita", "Ratatouille"),
        ("ratatouille", "Ratatouille", "Pizza Margarrita"),
    ],
)
@pytest.mark.django_db()
def test_search_filter_with_field_name(
    client, recipes, search_term, expected_recipe_name, unexpected_recipe_name
):
    recipe_url = reverse("recipe-list")
    response = client.get(recipe_url, {"search": search_term})
    data = response.data["results"]
    returned_name = data[0]["name"]
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert expected_recipe_name == returned_name
    assert unexpected_recipe_name not in returned_name


@pytest.mark.parametrize(
    "ordering_condition, recipe_name, avg_rating",
    [("avg_rating", "Pizza Margarrita", 3.2), ("-avg_rating", "Ratatouille", 4.0)],
)
@pytest.mark.django_db()
def test_ordering_filter_with_field_avg_rating(
    client, recipes, ordering_condition, recipe_name, avg_rating
):
    recipe_url = reverse("recipe-list")
    response = client.get(recipe_url, {"ordering": ordering_condition})
    data = response.data["results"]
    returned_name = data[0]["name"]
    returned_avg_rating = data[0]["avg_rating"]

    assert response.status_code == status.HTTP_200_OK
    assert returned_name == recipe_name
    assert returned_avg_rating == avg_rating


@pytest.mark.django_db()
def test_add_recipe_with_authorization(client, users):
    ingredient1 = Ingredient.objects.create(name="Apple")
    ingredient2 = Ingredient.objects.create(name="Flour")
    client.force_authenticate(user=users[0])
    data = {
        "name": "Apple Pie",
        "category": "dessert",
        "description": "Some fantastic Apple Pie",
        "steps": "1 step, 2 step, 3 step",
        "total_cooking_time": 120,
        "difficulty": "medium",
        "country": "USA",
        "ingredients": [ingredient1.id, ingredient2.id],
    }
    recipe_url = reverse("recipe-list")
    response = client.post(path=recipe_url, data=data)
    response_data = response.data

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data["name"] == data["name"]
    assert response_data["author"] == users[0].email


@pytest.mark.django_db()
def test_update_recipe_without_owner_permission(client, recipes, users):
    recipe = Recipe.objects.get(name="Ratatouille")
    data = {"difficulty": "easy"}

    client.force_authenticate(user=users[1])
    recipe_url = reverse("recipe-detail", kwargs={"slug": recipe.slug})
    response = client.patch(path=recipe_url, data=data)
    response_data = response.data

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response_data["detail"] == "You are not author of this recipe!"
