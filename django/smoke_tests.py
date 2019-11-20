""" /smoke_tests.py
    tests prerequisites for integrated/functional tests

    basically, nginx and postgresql server must be ready for all of those tests
"""
import pytest
from django.db import connections
from django.db.utils import OperationalError


@pytest.mark.smoke
@pytest.mark.django_db
class SmokeTest:

    def test_postgresql_ready(self):
        try:
            _ = connections['default'].cursor()
        except OperationalError:
            assert False, 'Postgres is not ready'
        else:
            assert True
