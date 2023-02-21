from django.contrib import admin

from .models import Link, Profile, Timeline

admin.site.register(Profile)
admin.site.register(Link)
admin.site.register(Timeline)
