""" /api/tests.py
    perform server-level isolated(using pytest-django live_server fixture) tests
"""
import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.unit
class HCTest:
    """
    tests views for health-check
    """
    def test_ping_pong(self, live_server):
        client = APIClient()
        response = client.get(live_server.url + '/api/ping/')  # without trailing slash(/$), it will return code 301
        assert response.status_code in (status.HTTP_200_OK, )
