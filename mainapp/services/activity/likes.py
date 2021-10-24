from django.template.loader import render_to_string
from mainapp.models import Likes


def new_like(self):
    if not Likes.objects.filter(article_id=int(self.kwargs["pk"]), user_id=self.request.user.pk):
        Likes.objects.create(article_id=self.kwargs["pk"], user_id=self.request.user.pk)


def change_like(self):
    new_like(self)
    like = Likes.objects.filter(article_id=int(self.kwargs["pk"]), user_id=self.request.user.pk).first()
    return like


def define_count_like(self):
    return len(Likes.objects.filter(article_id=int(self.kwargs["pk"]), status=True))


def if_status_like(like):
    if not like or like.status is False:
        like.status = True
    else:
        like.status = False
    like.save()
    return like


def view_like(self):
    like = change_like(self)
    like.count = define_count_like(self)
    return like


def set_like(self, context):
    like = change_like(self)
    like = if_status_like(like)
    like.count = define_count_like(self)
    context["likes"] = like
    result = render_to_string('mainapp/includes/inc__like.html', context=context, request=self.request)
    return result
