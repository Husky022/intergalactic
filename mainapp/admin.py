from django.contrib import admin

from mainapp.models import Article, Hub
from .models import AdvUser

admin.site.register(Article)
admin.site.register(Hub)

admin.site.register(AdvUser)
