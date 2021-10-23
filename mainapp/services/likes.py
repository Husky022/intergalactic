from django.template.loader import render_to_string
from mainapp.models import Likes


def render_like_count_user(self):
    like_items_article = Likes.objects.filter(article_id=int(self.kwargs["pk"]))
    like_items_article.user_like = like_items_article.filter(user_id=self.request.user.pk)
    like_items_article.like_count = like_items_article.filter(like_status=True).count()
    return like_items_article


def likes_view(self):
    like_items_article = render_like_count_user(self)
    if not like_items_article.user_like or like_items_article.user_like.filter(like_status=False):
        like_items_article.user_like_status = False
    else:
        like_items_article.user_like_status = True
    return like_items_article


def ajax_like(self, context, user_like, like_count, user_like_first):
    like_list = render_to_string('mainapp/includes/inc__like.html', context=context, request=self.request)
    if not user_like or user_like_first.like_status is False:
        like_count += 1
        user_like_first.like_status = True
    else:
        like_count -= 1
        user_like_first.like_status = False
    user_like_first.save()
    return user_like_first.like_status, like_list, like_count


def set_like(self, context):
    like_items_article = render_like_count_user(self)
    user_like_first = like_items_article.user_like.first()
    if not like_items_article.user_like:
        like_items_article.user_like = Likes.objects.create(article_id=self.kwargs["pk"], user_id=self.request.user.pk,
                                                            like_status=True)
    if self.request.is_ajax():
        print("AJAX")
        like_status, like_list, like_count = ajax_like(self, context, like_items_article.user_like,
                                                       like_items_article.like_count, user_like_first)
        return like_status, like_count
