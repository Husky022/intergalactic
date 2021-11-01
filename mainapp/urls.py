from django.urls import path

from .views import Main, Articles, ArticlePage, Search

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('articles/', Articles.as_view(), name='articles'),
    path('articles/<int:pk>/', Articles.as_view(), name='hub_category'),
    path('article_page/<int:pk>/', ArticlePage.as_view(), name='article_page'),
    path('search/', Search.as_view(), name='search'),
]
