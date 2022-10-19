import pytest

from ads.serializers import AdDetailSerializer


@pytest.mark.django_db
def test_detail(client, ad, user_token):
	response = client.get(
		f"/ad/{ad.id}/",
		HTTP_AUTHORIZATION=f"Bearer {user_token}")

	assert response.status_code == 200
	assert response.data == AdDetailSerializer(ad).data


@pytest.mark.django_db
def test_not_token_detail(client, ad):
	response = client.get(
		f"/ad/{ad.id}/",
	)

	assert response.status_code == 401
	assert response.json()['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_error_detail(client, user_token):
	response = client.get(
		"/ad/fgh/",
		HTTP_AUTHORIZATION=f"Bearer {user_token}")

	assert response.status_code == 404
