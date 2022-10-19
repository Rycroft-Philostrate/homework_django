import pytest

from tests.factories import AdFactory


@pytest.mark.django_db
def test_list(client):
	ads = AdFactory.create_batch(10)

	response = client.get("/ad/")

	ads_list = []
	for ad in ads:
		ads_list.append({
			"id": ad.id,
			"name": ad.name,
			"author_id": ad.author_id,
			"author": ad.author.first_name,
			"price": ad.price,
			"description": ad.description,
			"is_published": ad.is_published,
			"category_id": ad.category_id,
			"image": None
		})

	expected_response = {
		"items": ads_list,
		"num_pages": 10,
		"total": 10,
	}

	assert response.status_code == 200
	assert response.json() == expected_response


def test_error_list(client):

	response = client.get("/ads/")

	assert response.status_code == 404
