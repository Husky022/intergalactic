from django.contrib import admin

from mainapp.models import ArticlesCategory, Article, Hab
from .models import AdvUser

admin.site.register(ArticlesCategory)
admin.site.register(Article)
admin.site.register(Hab)

admin.site.register(AdvUser)
