from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Blog
from haystack.forms import SearchForm

from taggit_labels.widgets import LabelWidget
from taggit.forms import *
from taggit.models import Tag
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django.forms.extras.widgets import SelectDateWidget


class PostForm(forms.ModelForm):

    image = forms.ImageField(required = True)
    class Meta:
        model = Blog
        fields = ('title','description', 'image',)
        widgets = {

            'description': forms.Textarea(),

        }