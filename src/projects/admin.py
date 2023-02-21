from django.contrib import admin

from projects.models import Post, Profile, Tag

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Post)
