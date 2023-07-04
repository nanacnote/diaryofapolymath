from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestExclusiveModels:
    def test_XXX_model_has_expected_fields_and_constraints(self):
        pass


@pytest.mark.django_db
class TestExclusiveViews:
    def test_index_page_renders_correctly(self, client):
        response = client.get(reverse("exclusive:index"))

        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
class TestExclusiveUtils:
    def test_XXX_utility_as_a_unit(self):
        pass
