from django.test import TestCase
import requests
# Create your tests here.

url = f"https://api.tvmaze.com/shows/118"
response = requests.get(url)
show_data = response.json()


print(show_data['name'],
show_data['id'], show_data['genres'])