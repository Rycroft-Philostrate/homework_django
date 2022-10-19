import pytest


@pytest.mark.django_db
def test_create(client, user, category):
	expected_response = {
		'id': 1,
		'author': user.id,
		'category': category.id,
		'description': 'test text',
		'image': None,
		'is_published': False,
		'name': 'testnamett',
		'price': 100,
	}
	response = client.post(
		"/ad/create/",
		{
			"name": "testnamett",
			"price": 100,
			"description": "test text",
			"is_published": False,
			"author": user.id,
			"category": category.id
		},
	)

	assert response.status_code == 201
	assert response.data == expected_response


@pytest.mark.django_db
def test_error_is_published(client, user, category):
	response = client.post(
		"/ad/create/",
		{
			"name": "testnamett",
			"price": 100,
			"description": "test text",
			"is_published": True,
			"author": user.id,
			"category": category.id
		},
	)

	assert response.status_code == 400
	assert response.json()['is_published'] == ['Ad published can not be True']
