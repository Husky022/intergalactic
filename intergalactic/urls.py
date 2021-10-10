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
from authapp import urls as auth_urls

urlpatterns = [
    path('', mainapp.Main.as_view(), name='main'),
    path('articles/', mainapp.Articles.as_view(), name='articles'),
    path('article_page/<int:hub_pk>/', mainapp.article_page, name='article_page'),
    path('hub/<int:hub_pk>/', mainapp.hub, name='hub'),
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls, namespace='auth'))
]
