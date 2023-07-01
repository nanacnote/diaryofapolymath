from django.db import models

from about.models import Profile
from blog.managers import PostManager


class Tag(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        ordering = ["-published_on"]

    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    published_on = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)
    abstract = models.TextField()
    body = models.TextField()

    objects = PostManager()

    def __str__(self):
        return self.title
