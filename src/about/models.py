from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    image_title = models.CharField(max_length=25)
    image_alt = models.CharField(max_length=50)
    image_src_url = models.TextField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email


class Link(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    icon_title = models.CharField(max_length=25)
    icon_alt = models.CharField(max_length=50)
    icon_href = models.CharField(max_length=250)
    icon_src_url = models.TextField()

    def __str__(self):
        return self.icon_title


class Timeline(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    modified_on = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=120, unique=True)
    body = models.TextField()

    def __str__(self):
        return self.header
