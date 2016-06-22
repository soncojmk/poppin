from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Post
from haystack.forms import SearchForm
from taggit_labels.widgets import LabelWidget
from taggit.forms import *
from taggit.models import Tag

class PostForm(forms.ModelForm):
    time = forms.TimeField(required = True)
    photo = forms.ImageField(required = False)
    class Meta:
        model = Post
        fields = ('title', 'street_address', 'city', 'state', 'zip_code', 'date', 'time', 'description','price','photo','tags',)

#adds first name and last name to signup form
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()




class SearchForm(SearchForm):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(pub_date__gte=self.cleaned_data['start_date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(pub_date__lte=self.cleaned_data['end_date'])

        return 

class ContentForm(forms.ModelForm):
    tags = TagField(required=False, widget=LabelWidget)

