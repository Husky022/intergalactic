"""intergalactic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('articles/', mainapp.articles, name='articles'),
    path('article_page/<int:article_pk>/', mainapp.article_page, name='article_page'),
    path('article_category/<int:category_pk>/', mainapp.article_category, name='article_category'),
    path('programming/', mainapp.programming, name='programming'),
    path('webdesign/', mainapp.web_design_page, name='webdesign'),
    path('htmlcss/', mainapp.html_css_page, name='htmlcss'),
    path('admin/', admin.site.urls),
]
