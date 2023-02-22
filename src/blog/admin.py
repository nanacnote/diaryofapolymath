from django.contrib import admin

from blog.models import Author, Post, Tag

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post)
