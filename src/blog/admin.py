from django.contrib import admin

from blog.models import Post, Tag

admin.site.register(Tag)
admin.site.register(Post)
