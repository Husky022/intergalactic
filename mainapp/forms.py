from django_summernote.widgets import SummernoteWidget
from django.forms import ModelForm

from mainapp.models import Article
from django import forms


class ArticleCreationForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'preview', 'text', 'tag', 'hub', 'image']
        widgets = {
            'text': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(ArticleCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 1000px;'


class CommentForm(forms.Form):
    comment = forms.CharField(label='comment', max_length=1000)

class SubCommentForm(forms.Form):
    comment = forms.CharField(label='subcomment', max_length=1000)