from django.urls import re_path

import adminapp.views as adminapp

from .apps import AdminappConfig

app_name = AdminappConfig.name

urlpatterns = [
    re_path(r"^$", adminapp.admin_main, name="admin_main"),
    re_path(r"^users/create/$", adminapp.user_create, name="user_create"),
    re_path(r"^users/read/$", adminapp.UsersListView.as_view(), name="users"),
    re_path(r"^users/update/(?P<pk>\d+)/$", adminapp.user_update, name="user_update"),
    re_path(r"^users/delete/(?P<pk>\d+)/$", adminapp.user_delete, name="user_delete"),
    re_path(r"^users/blocked/(?P<pk>\d+)/$", adminapp.user_blocked, name="user_blocked"),
    re_path(r"^users/unblocked/(?P<pk>\d+)/$", adminapp.user_unblocked, name="user_unblocked")
]
