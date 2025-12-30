from django.contrib import admin

from .models import *
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)

# Register your models here.
