from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from mainapp.models import Article, Hub, Comment, Likes
from authapp.models import IntergalacticUser


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('text', )


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Hub)

admin.site.register(IntergalacticUser)
admin.site.register(Comment)
