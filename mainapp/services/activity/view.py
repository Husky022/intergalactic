from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy

from mainapp.models import Comment, SubComment
from mainapp.services.activity.likes import Like
from mainapp.services.activity.comment import parse_sub_comment, get_or_post, get_comment, delete


def fill_context(self):
    self.object = self.get_object()
    context = self.get_context_data(object=self.get_object())
    context['comments'] = Comment.objects.filter(article_id=self.kwargs["pk"], is_active=True)
    context['subcomments'] = parse_sub_comment(self)
    context['comments_count'] = len(context['comments']) + len(
        SubComment.objects.filter(article_id=self.kwargs["pk"], is_active=True))
    context['likes'] = Like(self.request, self.kwargs).view_like()
    return context


def article_page_get(self):
    context = fill_context(self)
    if self.request.is_ajax():
        if self.request.GET.dict().get("text_comment") or self.request.GET.dict().get("text_subcomment"):
            result = get_comment(self, context)
        elif self.request.GET.dict().get("com_delete") or self.request.GET.dict().get("sub_com_delete"):
            result = delete(self, self.request.GET.dict(), context)
        else:
            result = Like(self.request, self.kwargs, ).set_like(context)
        return JsonResponse({"result": result})
    return self.render_to_response(context)


def article_page_post(self):
    get_or_post(self, self.request.POST.dict())
    return HttpResponseRedirect(reverse_lazy('article_page', args=(int(self.kwargs["pk"]),)))


class Activity:
    types = {
        'get': article_page_get,
        'post': article_page_post,
    }

    @classmethod
    def create(cls, type_, *args, **kwargs):
        return cls.types[type_](*args, **kwargs)
