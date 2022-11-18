from django.forms import ModelForm
from .models import Post
from django import forms
class PostForm(ModelForm):
    class Meta :
        model =Post
        fields = ['title','content']
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )