from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from authapp.forms import IntergalacticUserLoginForm, IntergalacticUserRegisterForm, IntergalacticUserEditForm


def login(request):
    title = 'Вход'
    next_url = request.GET.get('next') if 'next' in request.GET.keys() else ''
    login_form = IntergalacticUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))
    content = {
        'title': title,
        'login_form': login_form,
        'next': next_url
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = IntergalacticUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = IntergalacticUserRegisterForm()
    content = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'Редактирование'

    if request.method == 'POST':
        edit_form = IntergalacticUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = IntergalacticUserEditForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form,
    }

    return render(request, 'authapp/edit.html', content)
