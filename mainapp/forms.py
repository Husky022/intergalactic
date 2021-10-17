from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(label='comment', max_length=1000)
