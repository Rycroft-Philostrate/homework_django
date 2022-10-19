import pytest


@pytest.mark.django_db
def test_create(client, user_token, user, ad):
	expected_response = {
		'id': 1,
		'name': 'test',
		'owner': user.id,
		'items': [ad.id],
	}

	response = client.post(
		"/selection/create/",
		{
			"name": "test",
			"owner": user.id,
			"items": [ad.id],
		},
		HTTP_AUTHORIZATION=f"Bearer {user_token}")

	assert response.status_code == 201
	assert response.data == expected_response
