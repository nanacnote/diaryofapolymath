from django.db import models


class Profile(models.Model):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
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
    body = models.TextField()

    def __str__(self):
        return self.title
