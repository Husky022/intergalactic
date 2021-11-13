from django.urls import path

import authapp.views as authapp


app_name = 'auth'

urlpatterns = [
    path('login/', authapp.LoginView.as_view(), name='login'),
    path('logout/', authapp.LogoutView.as_view(), name='logout'),
    path('register/', authapp.RegisterView.as_view(), name='register'),
    path('edit/', authapp.UserEditView.as_view(), name='edit'),
    path('notifications/', authapp.NotificationView.as_view(), name='notifications'),
    path('blocked/', authapp.BlockedView.as_view(), name='blocked')
]
