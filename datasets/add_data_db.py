from django.shortcuts import get_object_or_404

from homework_django.wsgi import *

from ads.models import Category, Ad
from users.models import Location, User

import json


with open('data_categories.json', encoding='utf-8') as json_file:
	data = json.load(json_file)
	for value in data:
		Category.objects.create(
			name=value["name"],
		)


with open('data_locations.json', encoding='utf-8') as json_file:
	data = json.load(json_file)
	for value in data:
		Location.objects.create(
			name=value["name"],
			lat=value["lat"],
			lng=value["lng"],
		)


with open('data_users.json', encoding='utf-8') as json_file:
	data = json.load(json_file)
	for value in data:
		user = User.objects.create(
			username=value["username"],
			password=value["password"],
			first_name=value["first_name"],
			last_name=value["last_name"],
			role=value["role"],
			age=value["age"],
		)

		location, _ = Location.objects.get_or_create(id=value["location_id"])
		user.locations.add(location)

with open('data_ads.json', encoding='utf-8') as json_file:
	data = json.load(json_file)
	for value in data:
		Ad.objects.create(
			name=value["name"],
			author_id=value["author_id"],
			price=value["price"],
			description=value["description"],
			is_published=value["is_published"] == 'TRUE',
			image=value["image"],
			category_id=value["category_id"],
		)
