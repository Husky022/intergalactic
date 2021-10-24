from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from mainapp.models import Comment, SubComment
from mainapp.services.activity.likes import view_like, set_like
from mainapp.services.activity.comment import parse_sub_comment, get_or_post


def fill_context(self):
    self.object = self.get_object()
    context = self.get_context_data(object=self.get_object())
    context['comments'] = Comment.objects.filter(article_id=self.kwargs["pk"])
    context['subcomments'] = parse_sub_comment(self)
    context['comments_count'] = len(context['comments']) + len(SubComment.objects.filter(article_id=self.kwargs["pk"]))
    context['likes'] = view_like(self)
    return context


def get_comment(self, context):
    get_or_post(self, self.request.GET.dict())
    context['comments'] = Comment.objects.filter(article_id=self.kwargs["pk"])
    context['subcomments'] = parse_sub_comment(self)
    return render_to_string('mainapp/includes/inc__comment.html', context, request=self.request)


def article_page_get(self):
    context = fill_context(self)
    if self.request.is_ajax():
        if self.request.GET.dict().get("text_comment") or self.request.GET.dict().get("text_subcomment"):
            result = get_comment(self, context)
        else:
            result = set_like(self, context)
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
