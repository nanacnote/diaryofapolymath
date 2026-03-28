from django.contrib import admin

from blog.models import Comment, Post, Tag

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
