""" /api/tests.py
    perform server-level isolated(using pytest-django live_server fixture) tests
"""
import pytest
from rest_framework import status
from rest_framework.test import APIClient


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

    def test_get_history_specific_item(self):
        # return specific history, and
        # get response and check it well came
        response = self.client.get(self.server_url + '/api/history/')
        assert response.status_code == status.HTTP_200_OK

        history_list = [model.aka for model in response.data.results]
        # check given resource has results list field
        assert isinstance(response.data.results, list)

        # it follows rules of list search url
        for item in history_list[:5]:
            for field in ('img', 'model', 'label', 'class'):
                assert field in item.keys(), 'Required field {} not found in {}'.format(field, item)

    def test_get_model_short_description(self):
        # return short descriptive preview such as available models, descriptions, test metrics
        # check status code is OK
        response = self.client.get(self.server_url + '/api/model/')
        assert response.status_code == status.HTTP_200_OK

        # it should contain list of item
        assert isinstance(response.data.results, list)

        # for every models, check it has must-have fields
        for model in response.data.results:
            keys = model.keys()
            for field in ('aka', 'name', 'short_desc', 'test_metrics'):
                assert field in keys, 'Field {} not in {}'.format(field, model)

    def test_get_model_detail_information(self):
        # return more detailed description of specific model, including visualization resources and more
        response = self.client.get(self.server_url + '/api/model/')
        assert response.status_code == status.HTTP_200_OK

        available_models = [model.aka for model in response.data.results]
        for model in available_models:
            # send request for detail information of specific model
            response = self.client.get(self.server_url + f'/api/model/{model}/')
            assert response.status_code == status.HTTP_200_OK

            # check fields are in response data
            keys = model.keys()
            for field in ('aka', 'name', 'description', 'test_metrics', 'visualization'):
                assert field in keys, "Model {} don't have field {}".format(model, field)

    def test_post_predict_image(self, client, live_server):
        # user request for prediction with data: image file, label of it, prediction model
        data = {
            'image': open('C:/Users/dldbc/Downloads/sample_image.jpg', mode='rb'),
            'label': 'Cat',
            'model': 'svm',
        }
        response = self.client.post(self.server_url + '/api/predict/', data=data)
        assert response.status_code == status.HTTP_201_CREATED

        # and it will return history object created
        pass
