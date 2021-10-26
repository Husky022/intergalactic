from django.template.loader import render_to_string

from authapp.models import IntergalacticUser
from mainapp.models import Likes, Article
from authapp.services.notifications import NewNotification


def new_like(self):
    article = Article.objects.filter(id=int(self.kwargs["pk"])).first()
    recipient = IntergalacticUser.objects.filter(id=article.author_id).first()
    NewNotification.create('like_article', recipient, self.request.user, None, article.name)
    if not Likes.objects.filter(article_id=int(self.kwargs["pk"]), user_id=self.request.user.pk):
        Likes.objects.create(article_id=self.kwargs["pk"], user_id=self.request.user.pk)



def change_like(self):
    if not self.request.user.is_anonymous:
        like = Likes.objects.filter(article_id=int(self.kwargs["pk"]), user_id=self.request.user.pk).first()
    else:
        if Likes.objects.filter(article_id=int(self.kwargs["pk"])):
            like = Likes.objects.filter(article_id=int(self.kwargs["pk"])).first()
        else:
            return None
    return like


def define_count_like(self, status):
    return len(Likes.objects.filter(article_id=int(self.kwargs["pk"]), status=status))


def status_like(like, status):
    if like.status == status:
        like.status = "UND"
    else:
        like.status = status
    like.save()
    return like


def view_like(self):
    like = change_like(self)
    if like:
        like.like_count = define_count_like(self, "LK")
        like.dislike_count = define_count_like(self, "DZ")
        return like
    return None


def set_like(self, context):
    new_like(self)
    like = change_like(self)
    like = status_like(like, self.request.GET.dict()["status"])
    like.like_count = define_count_like(self, "LK")
    like.dislike_count = define_count_like(self, "DZ")
    context["likes"] = like
    result = render_to_string('mainapp/includes/inc__activity.html', context=context, request=self.request)
    return result
