from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from authapp.forms import IntergalacticUserLoginForm, IntergalacticUserRegisterForm, IntergalacticUserEditForm
from django.views.generic import FormView, ListView
from django.views.generic.base import View
from django.db import transaction

from authapp.models import Notification
from mainapp.models import Article
from mainapp.forms import ArticleCreationForm


class LoginView(FormView):
    template_name = 'authapp/login.html'
    form_class = IntergalacticUserLoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(self.request, user)

        return super().form_valid(form)


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
    redirect_to = 'auth:profile'
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


class UserProfileView(View):
    title = 'личный кабинет'
    template_name = 'authapp/profile.html'

    def get_context_data(self):
        articles = Article.objects.filter(author=self.request.user)
        articles_with_form = []
        for article in articles:
            # добавляем форму к объектам товаров, нужно для редактирования
            articles_with_form.append({
                'article': article,
                'form': ArticleCreationForm(instance=article)
            })

        context = {
            'title': self.title,
            'user': self.request.user,
            'creation_form': ArticleCreationForm(),
            'articles': articles_with_form,
            'role': "Администратор" if self.request.user.is_superuser else "Пользователь",
        }
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class NotificationView(ListView):
    title = 'Уведомления'
    template_name = 'authapp/notifications.html'

    def get_context_data(self, **kwargs):
        notifications = Notification.objects.filter(recipient_id=self.request.user.id)
        context = {
            'title': self.title,
            'user': self.request.user,
            'notifications': notifications,
        }
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())