import re
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView
from mainapp.services.commentsparse import comment

from mainapp.models import Article


# def index(request):
#     template = loader.get_template('moderator.html')
#     context ={'title':title}
#     return HttpResponse(template.render(context, request))

class Moderator(ListView):
    model = Article
    template_name = 'moderator/moderator.html'
    extra_context = {'title': 'Модератор'}
    paginate_by = 5

    def get_queryset(self):
        queryset = comment(self)
        return queryset
