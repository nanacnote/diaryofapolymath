from http import HTTPStatus

import pytest
from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError
from django.urls import reverse

from about.models import Link, Profile, Timeline


@pytest.mark.django_db
class TestAboutModels:
    @pytest.mark.parametrize(
        "field_name, field_value, error_message",
        [
            ("username", "username", "UNIQUE"),
            ("email", "email", "UNIQUE"),
            ("image_title", None, "NOT NULL"),
            ("image_alt", None, "NOT NULL"),
            ("image_src_url", None, "NOT NULL"),
        ],
    )
    @pytest.mark.parametrize("factory_class", ["ProfileFactory"], indirect=True)
    def test_profile_model_has_expected_fields_and_constraints(
        self, factory_class, field_name, field_value, error_message
    ):
        allowed_fields = ["id", "image_title", "image_alt", "image_src_url"] + [
            field.name for field in AbstractUser._meta.get_fields()
        ]
        profile = Profile.objects.first()
        with pytest.raises(IntegrityError) as error:
            factory_class.create(
                **{
                    field_name: getattr(profile, field_value)
                    if hasattr(profile, str(field_value))
                    else field_value
                }
            )
        assert error_message in str(error.value)
        assert len(Profile._meta._get_fields(reverse=False)) == len(allowed_fields)
        assert str(profile) == profile.name
        assert profile.name == f"{profile.first_name} {profile.last_name}"
        assert all(hasattr(Profile, attr) for attr in allowed_fields)

    @pytest.mark.parametrize(
        "field_name, field_value, error_message",
        [
            ("icon_title", None, "NOT NULL"),
            ("icon_alt", None, "NOT NULL"),
            ("icon_href", None, "NOT NULL"),
            ("icon_src_url", None, "NOT NULL"),
        ],
    )
    @pytest.mark.parametrize("factory_class", ["LinkFactory"], indirect=True)
    def test_link_model_has_expected_fields_and_constraints(
        self, factory_class, field_name, field_value, error_message
    ):
        allowed_fields = ["id", "profile", "icon_title", "icon_alt", "icon_href", "icon_src_url"]
        link = Link.objects.first()
        with pytest.raises(IntegrityError) as error:
            factory_class.create(
                **{
                    field_name: getattr(link, field_value)
                    if hasattr(link, str(field_value))
                    else field_value
                }
            )
        assert error_message in str(error.value)
        assert len(Link._meta._get_fields(reverse=False)) == len(allowed_fields)
        assert str(link) == link.icon_title
        assert all(hasattr(Link, attr) for attr in allowed_fields)

    @pytest.mark.parametrize(
        "field_name, field_value, error_message",
        [
            ("header", "header", "UNIQUE"),
            ("body", None, "NOT NULL"),
        ],
    )
    @pytest.mark.parametrize("factory_class", ["TimelineFactory"], indirect=True)
    def test_timeline_model_has_expected_fields_and_constraints(
        self,
        factory_class,
        field_name,
        field_value,
        error_message,
    ):
        allowed_fields = ["id", "profile", "created_on", "modified_on", "header", "body"]
        timeline = Timeline.objects.first()
        with pytest.raises(IntegrityError) as error:
            factory_class.create(
                **{
                    field_name: getattr(timeline, field_value)
                    if hasattr(timeline, str(field_value))
                    else field_value
                }
            )
        assert error_message in str(error.value)
        assert len(Timeline._meta._get_fields(reverse=False)) == len(allowed_fields)
        assert str(timeline) == timeline.header
        assert all(hasattr(Timeline, attr) for attr in allowed_fields)


@pytest.mark.django_db
class TestAboutViews:
    def test_index_page_renders_correctly(self, client):
        response = client.get(reverse("about:index"))
        assert response.status_code == HTTPStatus.OK
        assert all(
            attr in [template.name for template in response.templates]
            for attr in ["base/index.html", "about/index.html"]
        )
        assert all(attr in response.context for attr in ["profile", "links", "timelines"])


@pytest.mark.django_db
class TestAboutUtils:
    def test_XXX_utility_as_a_unit(self):
        assert 1 == 2
