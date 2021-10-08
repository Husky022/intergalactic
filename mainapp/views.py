from django.shortcuts import render
from datetime import datetime
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from django.shortcuts import render

# Create your views here.

def base(request):
    context = {
        'now': datetime.now().year
    }
    return render(request, 'mainapp/base.html', context)

def main(request):
    context = {}
    return render(request, 'mainapp/index.html', context)

def programming(request):
    context = {
        'title': 'Программирование'
    }
    return render(request, 'mainapp/category_base.html', context)

def web_design_page(request):
    context = {
        'title': 'Веб-Дизайн'
    }
    return render(request, 'mainapp/category_base.html', context)

def html_css_page(request):
    context = {
        'title': 'HTML/CSS'
    }
    return render(request, 'mainapp/category_base.html', context)

