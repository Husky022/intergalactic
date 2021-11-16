from django.urls import path
import mainapp.views as mainapp

from .views import Main, Articles, ArticlePage, Search

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('articles/<int:pk>/', Articles.as_view(), name='hub_category'),
    path('article_page/<int:pk>/', ArticlePage.as_view(), name='article_page'),
    path('comment/<int:pk>/', mainapp.like_dislike_comment, name='comments'),
    path('search/', Search.as_view(), name='search'),
    path('set_sorting/<str:sorting_type>/', mainapp.set_sorted_type, name='set_sorting'),
]
