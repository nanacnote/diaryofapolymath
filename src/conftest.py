# https://github.com/pytest-dev/pytest-django

import datetime
import inspect
import sys

import factory
import pytest
from django.template.defaultfilters import slugify

from about.models import Link, Profile, Timeline
from blog.models import Post, Tag

# --------------------------
# ABOUT APP MODEL FACTORIES
# --------------------------


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "p455w0rd")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    image_title = factory.Faker("word")
    image_alt = factory.Faker("word")
    image_src_url = factory.Faker("url")


class LinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Link

    profile = factory.SubFactory(ProfileFactory)
    icon_title = factory.Faker("word")
    icon_alt = factory.Faker("word")
    icon_href = factory.Faker("url")
    icon_src_url = factory.Faker("url")


class TimelineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Timeline

    profile = factory.SubFactory(ProfileFactory)
    header = factory.Faker("sentence")
    body = factory.Faker("paragraph")


# -------------------------
# BLOG APP MODEL FACTORIES
# -------------------------


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(ProfileFactory)
    title = factory.Faker("sentence")
    subtitle = factory.Faker("sentence")
    meta_description = factory.Faker("sentence")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    published_on = factory.Faker("date_time_this_year", tzinfo=datetime.timezone.utc)
    published = factory.Faker("boolean")
    abstract = factory.Faker("paragraph")
    body = factory.Faker("paragraph")

    # tags field with a ManyToMany relationship
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)


# ---------
# FIXTURES
# ---------
@pytest.fixture(scope="function")
def factory_class(request):
    """gives access to a model factory instance(s) given the classname(s)"""
    module, factories = sys.modules[__name__], []
    param_list = request.param if isinstance(request.param, list) else [request.param]
    for param in param_list:
        factory = next(
            (value for key, value in inspect.getmembers(module, inspect.isclass) if key == param),
            None,
        )
        if factory is None:
            raise ValueError(f"No factory found with name '{param}'")
        factories.append(factory)
    return factories[0] if not isinstance(request.param, list) else factories


@pytest.fixture(scope="session")
def about_app_seeds():
    profile = ProfileFactory.build(is_staff=True, is_superuser=True)
    links = LinkFactory.build_batch(3, profile=profile)
    timelines = TimelineFactory.build_batch(3, profile=profile)
    return (profile, links, timelines)


@pytest.fixture(scope="session")
def blog_app_seeds():
    tags = TagFactory.build_batch(3)
    posts = PostFactory.build(published=True, tags=tags)
    return (tags, posts)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker, about_app_seeds, blog_app_seeds):
    """override and extends the inbuilt `django_db_setup` fixture"""
    with django_db_blocker.unblock():
        # seed the db with a profile
        profile, links, timelines = about_app_seeds
        profile.save()
        for inst in links + timelines:
            inst.save()
        # seed the db with 1 post and 3 tags
        tags, posts = blog_app_seeds
        for inst in tags:
            inst.save()
        posts.author = profile
        posts.save()
