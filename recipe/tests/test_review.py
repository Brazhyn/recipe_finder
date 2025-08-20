from django.urls import reverse

import pytest
from rest_framework import status

from recipe.models import Recipe, Review


@pytest.fixture
def reviews(recipes, users):
    reviews = [
        Review.objects.create(
            author=users[1],
            description="This is a pretty delicious recipe.",
            rating=4,
            recipe=recipes[0],
        ),
        Review.objects.create(
            author=users[1],
            description="My kids liked it",
            rating=3,
            recipe=recipes[1],
        ),
    ]
    reviews = sorted(reviews, key=lambda review: review.rating, reverse=True)
    return reviews


@pytest.mark.django_db
def test_get_reviews_for_particular_recipe(client, recipes, reviews):
    reviews_url = reverse("review-list", kwargs={"slug": recipes[0].slug})
    response = client.get(reviews_url)
    data = response.data
    review = Review.objects.get(id=data[0]["id"])

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["id"] == reviews[0].id
    assert review.recipe.id == recipes[0].id


@pytest.mark.django_db
def test_user_cannot_review_same_recipe_twice(client, users, reviews, recipes):
    client.force_authenticate(user=users[1])
    data = {"description": "SOOO tasty", "rating": 5}
    reviews_url = reverse("review-list", kwargs={"slug": recipes[0].slug})
    response = client.post(reviews_url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == "You have already reviewed this movie!"


@pytest.mark.django_db
def test_recipe_rating_and_review_count_update(client, users, recipes, reviews):
    client.force_authenticate(user=users[0])
    data = {"description": "This is a pretty delicious recipe.", "rating": 4}
    reviews_url = reverse("review-list", kwargs={"slug": recipes[0].slug})
    response = client.post(reviews_url, data=data)
    recipe = Recipe.objects.get(slug=recipes[0].slug)
    print(recipe.avg_rating)

    assert response.status_code == status.HTTP_201_CREATED
    assert recipe.number_reviews == 1
    assert recipe.avg_rating == 4.0
