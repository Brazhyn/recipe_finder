import pytest
import datetime
from django.utils import timezone
from django.urls import reverse
from recipe.models import Recipe, Ingredient
from rest_framework.test import APIClient



"""-----------Fixtures------------"""
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email="michael2004@gmail.com",
        first_name="Michael",
        last_name="Row",
        phone="0987538747",
        password="qwerty123"
    )
    

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
            Ingredient.objects.create(name="Basil", caloric_content=23)
        ]
    }
    return ingredients
    

@pytest.fixture
def recipes(user, ingredients):
    recipes = [
        Recipe.objects.create(
            name="Pizza Margarrita",
            category="lunch",
            description = "some fantastic pizza",
            steps = "1 step, 2 step, 3 step",
            total_cooking_time=60,
            difficulty="medium",
            country="Italy",
            avg_rating=3.2,
            author=user
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
            author=user
        )  
    ]
    
    recipes[0].ingredients.set(ingredients["pizza"])
    recipes[0].date_created = timezone.now()
    recipes[0].save()
    
    recipes[1].ingredients.set(ingredients["ratatouille"])
    recipes[1].date_created = timezone.now() - datetime.timedelta(seconds=30)
    recipes[1].save()
    recipes = sorted(recipes, key=lambda r: r.date_created, reverse=True)
    return recipes


    
"""----------------Tests-----------------""" 
@pytest.mark.django_db
def test_recipe_empty_list(client):
    recipe_url = reverse("recipe-list")
    response = client.get(recipe_url)
    data = response.data["results"]
    
    assert response.status_code == 200
    assert data == []
    

@pytest.mark.django_db
def test_get_recipe_list(client, recipes):
    recipe_url = reverse("recipe-list")
    response = client.get(recipe_url)
    data = response.data["results"]
    
    assert response.status_code == 200
    assert len(data) == len(recipes)
    assert data[0]["id"] == recipes[0].id 
    assert data[0]["name"] == recipes[0].name
    assert data[0]["category"] == recipes[0].category
    assert data[0]["author"] == recipes[0].author.email
    

@pytest.mark.parametrize("search_term, expected_recipe_name, unexpected_recipe_name", [
    ("pizza", "Pizza Margarrita", "Ratatouille"),
    ("ratatouille", "Ratatouille", "Pizza Margarrita"),
])    
@pytest.mark.django_db()  
def test_search_filter_with_field_name(client, recipes, search_term, expected_recipe_name, unexpected_recipe_name):
    recipe_url = reverse("recipe-list")
    response = client.get(recipe_url, {"search": search_term})
    data = response.data["results"]
    returned_name = data[0]["name"]
    assert response.status_code == 200
    assert len(data) == 1
    assert expected_recipe_name == returned_name
    assert unexpected_recipe_name not in returned_name
    

@pytest.mark.parametrize("ordering_condition, recipe_name, avg_rating", [
    ("avg_rating", "Pizza Margarrita", 3.2),
    ("-avg_rating", "Ratatouille", 4.0)
])
@pytest.mark.django_db()  
def test_ordering_filter_with_field_avg_rating(client, recipes, ordering_condition, recipe_name, avg_rating):
    recipe_url = reverse("recipe-list")
    response = client.get(recipe_url, {"ordering": ordering_condition})
    data = response.data["results"]
    returned_name = data[0]["name"]
    returned_avg_rating = data[0]["avg_rating"]
    
    assert response.status_code == 200
    assert returned_name == recipe_name
    assert returned_avg_rating == avg_rating
    
    
@pytest.mark.django_db()  
def test_add_recipe_with_authorization(client, user):
    ingredient1 = Ingredient.objects.create(name="Apple")
    ingredient2 = Ingredient.objects.create(name="Flour")
    client.force_authenticate(user=user)
    data = {
        "name": "Apple Pie",
        "category": "dessert",
        "description": "Some fantastic Apple Pie",
        "steps": "1 step, 2 step, 3 step",
        "total_cooking_time": 120,
        "difficulty": "medium",
        "country": "USA",
        "ingredients": [ingredient1.id, ingredient2.id]
    }
    recipe_url = reverse("recipe-list")
    response = client.post(path=recipe_url, data=data)
    response_data = response.data
    
    assert response.status_code == 201
    assert response_data["name"] == data["name"]
    assert response_data["author"] == user.email 
    

@pytest.mark.django_db()
def test_update_recipe_without_owner_permission(client, recipes, user, django_user_model):
    test_user = django_user_model.objects.create_user(
        email="edward1995@gmail.com",
        first_name="Edward",
        last_name="Presley",
        phone="0962508147",
        password="qwerty123"
    )
    recipe = Recipe.objects.get(name="Ratatouille")
    data = {"difficulty": "easy"}
    
    client.force_authenticate(user=test_user)
    recipe_url = reverse("recipe-detail", kwargs={"slug": recipe.slug})
    response = client.patch(path=recipe_url, data=data)
    response_data = response.data
    
    assert response.status_code == 403
    assert response_data["detail"] == "You are not author of this recipe!"
    

    
    


        


        
        
    
    
