import os

import requests
from dotenv import load_dotenv

from recipe.models import Recipe

load_dotenv()


class DailyRecipesService:
    def __init__(self, location: str):
        self.location = location

    def get_daily_recipes(self):
        temperature = self.get_temperature()
        if temperature >= 25:
            return Recipe.objects.filter(
                category__in=["healthy", "salad", "appetizer"],
            ).order_by("-avg_rating")[:20]
        elif temperature <= 10:
            return Recipe.objects.filter(
                category__in=["soup", "drink", "lunch"],
            ).order_by("-avg_rating")[:20]
        else:
            return Recipe.objects.filter(
                category__in=["breakfast", "side_dish", "bread", "dessert"],
            ).order_by("-avg_rating")[:20]

    def get_temperature(self):
        url = "https://api.tomorrow.io/v4/weather/realtime"
        headers = {"apikey": os.getenv("TOMORROW_IO_API_KEY")}

        params = {
            "location": self.location,
            "language": "en",
            "fields": ["temperature"],
        }

        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()["data"]
        temperature = int(data["values"]["temperature"])

        return temperature
