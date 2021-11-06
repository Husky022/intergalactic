from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from authapp.forms import IntergalacticUserLoginForm, IntergalacticUserRegisterForm, IntergalacticUserEditForm
from django.views.generic import FormView, ListView
from django.views.generic.base import View
from django.db import transaction

from authapp.models import NotificationModel, IntergalacticUser
from authapp.services.notifications import Notification
from mainapp.models import Article, ArticleStatus
from mainapp.forms import ArticleCreationForm
from moderation.models import BlockedUser


class LoginView(FormView):
    template_name = 'authapp/login.html'
    form_class = IntergalacticUserLoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            blocked = BlockedUser.objects.all()
            if blocked:
                for b_usr in blocked:
                    if b_usr.user == user:
                        return redirect('auth:blocked')
                    else:
                        auth.login(self.request, user)
            else:
                auth.login(self.request, user)

        return super().form_valid(form)


class BlockedView(View):
    template_name = 'authapp/blocked.html'
    model = BlockedUser

    def get(self, request):
        return render(request, self.template_name)


class LogoutView(View):
    redirect_to = 'main'

    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse(self.redirect_to))


class RegisterView(FormView):
    title = 'регистрация'
    template_name = 'authapp/register.html'
    form_class = IntergalacticUserRegisterForm
    success_url = reverse_lazy('main')
    redirect_with_args = ['successful_register']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('auth:login'))


class UserEditView(View):
    title = 'редактирование'
    template_name = 'authapp/edit.html'
    redirect_to = 'profile:main'
    account_form = IntergalacticUserEditForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = {
            'title': self.title,
            'form': self.account_form(instance=self.request.user),
        }
        return context

    @transaction.atomic
    def post(self, request):
        edit_account_form = self.account_form(data=request.POST, files=request.FILES, instance=request.user)
        if edit_account_form.is_valid():
            edit_account_form.save()
            return HttpResponseRedirect(reverse(self.redirect_to))

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


def reading_notifications(func):
    def wrapper(self, request, **kwargs):
        res = func(self, request, **kwargs)
        notifications_not_read = NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0)
        for item in notifications_not_read:
            item.is_read = 1
            item.save()
        return res

    return wrapper


class NotificationView(ListView):
    title = 'Уведомления'
    template_name = 'authapp/notifications.html'
    ordering = ['-add_datetime']

    def get_context_data(self, **kwargs):
        notifications_not_read = NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0)
        notifications_read = NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=1)

        context = {
            'title': self.title,
            'user': self.request.user,
            'notifications_not_read': notifications_not_read.order_by('-add_datetime'),
            'notifications_read': notifications_read.order_by('-add_datetime')
        }
        return context

    @reading_notifications
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())
