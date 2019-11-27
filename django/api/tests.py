""" /api/tests.py
    perform server-level isolated(using pytest-django live_server fixture) tests

    testing strategy:
    - what would be most efficient and proper way API behavior?
        - response data format, fields, ...: duck-typing?
        - headers?

"""
import random
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from core.models import History


@pytest.fixture(scope='session')
def client():
    _client = APIClient()
    return _client


@pytest.mark.unit
@pytest.mark.api
class HCTest:
    """
    tests views for health-check
    """
    def test_ping_pong(self, client, live_server):
        response = client.get(live_server.url + '/api/ping/')  # without trailing slash(/$), it will return code 301
        assert response.status_code in (status.HTTP_200_OK, )


@pytest.mark.unit
@pytest.mark.api
@pytest.mark.django_db
class APITest:
    """
    tests views for model prediction API
    """
    @pytest.fixture(autouse=True)
    def _inject_fixtures(self, request):
        """
        inject some fixtures frequently used into class attribute
        """
        setattr(self, 'server_url', request.getfixturevalue('live_server').url)
        setattr(self, 'client', request.getfixturevalue('client'))

    def test_get_model_items(self):
        # check status code is OK
        response = self.client.get(self.server_url + '/api/model/')
        assert response.status_code == status.HTTP_200_OK

        # it should contain list of item
        items = response.data['results']
        assert isinstance(items, list) and len(items) > 0

    def test_post_predict_image(self):
        # user request for prediction with data: image file, label of it, prediction model
        fp = open('C:/Users/dldbc/Downloads/sample_image.jpg', mode='rb')
        data = {
            'img': fp,
            'label': 'cat',
            'model': 'svm',
        }
        response = self.client.post(self.server_url + '/api/history/', data=data)
        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_get_history_items(self):
        # get response and check it well came
        response = self.client.get(self.server_url + '/api/history/')
        assert response.status_code == status.HTTP_200_OK

        # check given resource has results list field
        items = response.data['results']
        assert isinstance(items, list)

        # each item retrieve check
        for item in items[:5]:
            response = self.client.get(item['url'])
            assert response.status_code == status.HTTP_200_OK
