from django.urls import path
from .views import Main, Articles, ArticlePage, ArticleCreationView, ArticleChangeActiveView, ArticleEditView

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('articles/', Articles.as_view(), name='articles'),
    path('articles/<int:pk>/', Articles.as_view(), name='hub_category'),
    path('article_page/<int:pk>/', ArticlePage.as_view(), name='article_page'),
    path('create_article/', ArticleCreationView.as_view(), name='create_article'),
    path('change_active/<int:article_pk>/', ArticleChangeActiveView.as_view(), name='change_active'),
    path('edit_active/<int:article_pk>/', ArticleEditView.as_view(), name='edit_article'),

]
