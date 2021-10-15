from django.contrib import admin

from mainapp.models import Article, Hub, Comment
from authapp.models import IntergalacticUser


admin.site.register(Article)
admin.site.register(Hub)

admin.site.register(IntergalacticUser)
admin.site.register(Comment)
