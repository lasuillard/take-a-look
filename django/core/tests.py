""" /core/tests.py
    test primarily for ORM models
"""
import pytest
from . import models


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.django_db
class ModelTest:

    def test_history_delete_image_on_delete(self):
        pass
