from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from mainapp.models import Article, Hub, Comment, Likes, ArticleStatus, Sorting, VoiceArticle
from authapp.models import IntergalacticUser
from moderation.models import BlockedUser


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Hub)
admin.site.register(BlockedUser)
admin.site.register(ArticleStatus)
admin.site.register(IntergalacticUser)
admin.site.register(Comment)
admin.site.register(Sorting)
admin.site.register(VoiceArticle)
