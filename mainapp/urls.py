from django.urls import path

import mainapp.views as mainapp
from .views import Main, Articles, ArticlePage, ArticleCreationView, ArticleChangeActiveView, ArticleEditView, \
    SendToModeration, DraftArticle, ArticlesScroll
from .views import Main, Articles, ArticlePage, ArticleCreationView, ArticleChangeActiveView, ArticleEditView, Search

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('articles/', Articles.as_view(), name='articles'),
    path('articles/<int:pk>/', Articles.as_view(), name='hub_category'),
    path('article_page/<int:pk>/', ArticlePage.as_view(), name='article_page'),
    path('create_article/', ArticleCreationView.as_view(), name='create_article'),
    path('change_active/<int:article_pk>/', ArticleChangeActiveView.as_view(), name='change_active'),
    path('edit_article/<int:pk>/', ArticleEditView.as_view(), name='edit_article'),
    path('send_to_moderation/<int:pk>/', SendToModeration.as_view(), name='send_to_moderation'),
    path('draft_article/<int:pk>/', DraftArticle.as_view(), name='draft_article'),
    path('article_scroll/', ArticlesScroll.as_view(), name='article_scroll'),
    path('article_scroll/<int:pk>/', ArticlesScroll.as_view(), name='hub_category_scroll'),

    path('search/', Search.as_view(), name='search'),
]
