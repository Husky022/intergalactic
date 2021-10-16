from django import forms

from mainapp.models import Article, Comment

class CommentForm(forms.Form):
    comment = forms.CharField(label='comment', max_length=1000)