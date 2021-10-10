from django.contrib import admin

from mainapp.models import ArticlesCategory, Article, Hab
from authapp.models import IntergalacticUser

admin.site.register(ArticlesCategory)
admin.site.register(Article)
admin.site.register(Hab)

admin.site.register(IntergalacticUser)
