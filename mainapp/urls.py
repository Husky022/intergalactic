from django.urls import path
from .views import Main, Articles, index, article_page, hub

urlpatterns = [
    path('', index, name='index'),
    path('', Main.as_view(), name='main'),
    path('articles/', Articles.as_view(), name='articles'),
    path('article_page/<int:article_pk>/',
         article_page, name='article_page'),
    path('article_category/<int:category_pk>/',
         hub, name='article_category'),
]
