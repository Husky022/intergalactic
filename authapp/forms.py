from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django_summernote.widgets import SummernoteWidget
from authapp.models import IntergalacticUser


class IntergalacticUserLoginForm(AuthenticationForm):
    class Meta:
        model = IntergalacticUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(IntergalacticUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class IntergalacticUserRegisterForm(UserCreationForm):
    class Meta:
        model = IntergalacticUser
        fields = (
            'username',
            'first_name',
            'password1',
            'password2',
            'email',
            'age',
            'sex',
            'about_me',
            'avatar'
        )
        widgets = {
            'about_me': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(IntergalacticUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            self.fields[field_name].help_text = None


class IntergalacticUserEditForm(UserChangeForm):
    class Meta(object):
        model = IntergalacticUser
        fields = ('username', 'first_name', 'about_me', 'email', 'age', 'avatar')
        widgets = {
            'about_me': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(IntergalacticUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
