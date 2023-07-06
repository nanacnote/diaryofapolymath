from http import HTTPStatus

import pytest
from django.db import IntegrityError
from django.urls import reverse

from blog.models import Post, Tag


@pytest.mark.django_db
class TestBlogModels:
    @pytest.mark.parametrize(
        "field_name, field_value, error_message",
        [
            ("name", "name", "UNIQUE"),
            ("slug", "slug", "UNIQUE"),
        ],
    )
    @pytest.mark.parametrize("factory_class", ["TagFactory"], indirect=True)
    def test_tag_model_has_expected_fields_and_constraints(
        self, factory_class, field_name, field_value, error_message
    ):
        allowed_fields = ["id", "name", "slug"]
        tag = Tag.objects.first()
        with pytest.raises(IntegrityError) as error:
            factory_class.create(
                **{
                    field_name: getattr(tag, field_value)
                    if hasattr(tag, str(field_value))
                    else field_value
                }
            )
        assert error_message in str(error.value)
        assert len(Tag._meta._get_fields(reverse=False)) == len(allowed_fields)
        assert str(tag) == tag.name
        assert all(hasattr(Tag, attr) for attr in allowed_fields)

    @pytest.mark.parametrize(
        "field_name, field_value, error_message",
        [
            ("title", "title", "UNIQUE"),
            ("slug", "slug", "UNIQUE"),
            ("abstract", None, "NOT NULL"),
            ("body", None, "NOT NULL"),
        ],
    )
    @pytest.mark.parametrize("factory_class", ["PostFactory"], indirect=True)
    def test_post_model_has_expected_fields_and_constraints(
        self, factory_class, field_name, field_value, error_message
    ):
        allowed_fields = [
            "id",
            "author",
            "tags",
            "title",
            "subtitle",
            "meta_description",
            "slug",
            "created_on",
            "modified_on",
            "published_on",
            "published",
            "abstract",
            "body",
        ]
        post = Post.objects.first()
        with pytest.raises(IntegrityError) as error:
            factory_class.create(
                **{
                    field_name: getattr(post, field_value)
                    if hasattr(post, str(field_value))
                    else field_value
                }
            )
        assert error_message in str(error.value)
        assert len(Post._meta._get_fields(reverse=False)) == len(allowed_fields)
        assert str(post) == post.title
        assert all(hasattr(Post, attr) for attr in allowed_fields)


@pytest.mark.django_db
class TestBlogViews:
    def test_index_page_renders_correctly(self, client):
        response = client.get(reverse("blog:index"))

        assert response.status_code == HTTPStatus.OK
        assert all(
            attr in [template.name for template in response.templates]
            for attr in [
                "base/index.html",
                "blog/index.html",
                "blog/partials/aside_menu.html",
                "blog/partials/post_tags.html",
                "blog/partials/post_stats.html",
            ]
        )
        assert all(attr in response.context for attr in ["posts", "tags", "archives"])

    @pytest.mark.parametrize("factory_class", ["PostFactory"], indirect=True)
    def test_post_page_renders_correctly(self, client, factory_class):
        post = factory_class.create(published=True)
        response = client.get(reverse("blog:post", kwargs={"slug": post.slug}))

        assert response.status_code == HTTPStatus.OK
        assert all(
            attr in [template.name for template in response.templates]
            for attr in [
                "base/index.html",
                "blog/post.html",
                "blog/partials/aside_menu.html",
                "blog/partials/post_tags.html",
                "blog/partials/post_stats.html",
                "blog/partials/post_cta.html",
            ]
        )
        assert all(
            attr in response.context for attr in ["post", "prev", "next", "tags", "archives"]
        )

    @pytest.mark.parametrize("factory_class", ["PostFactory"], indirect=True)
    def test_archive_page_renders_correctly(self, client, factory_class):
        post = factory_class.create(published=True)
        response = client.get(reverse("blog:archive", kwargs={"slug": post.published_on.year}))

        assert response.status_code == HTTPStatus.OK
        assert all(
            attr in [template.name for template in response.templates]
            for attr in [
                "base/index.html",
                "blog/archive.html",
                "blog/partials/aside_menu.html",
                "blog/partials/post_tags.html",
                "blog/partials/post_stats.html",
            ]
        )
        assert all(attr in response.context for attr in ["posts", "tags", "archives"])

    @pytest.mark.parametrize("factory_class", [["TagFactory", "PostFactory"]], indirect=True)
    def test_tag_page_renders_correctly(self, client, factory_class):
        tf, pf = factory_class
        tag = tf.create()
        _ = pf.create(published=True, tags=[tag])
        response = client.get(reverse("blog:tag", kwargs={"slug": tag.slug}))

        assert response.status_code == HTTPStatus.OK
        assert all(
            attr in [template.name for template in response.templates]
            for attr in [
                "base/index.html",
                "blog/tag.html",
                "blog/partials/aside_menu.html",
                "blog/partials/post_tags.html",
                "blog/partials/post_stats.html",
            ]
        )
        assert all(attr in response.context for attr in ["posts", "tags", "archives"])


@pytest.mark.django_db
class TestBlogUtils:
    def test_XXX_utility_as_a_unit(self):
        pass
