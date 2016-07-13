from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, EventComment, Question, QuestionComment, Profile
from haystack.forms import SearchForm
from taggit_labels.widgets import LabelWidget
from taggit.forms import *
from taggit.models import Tag
from django.contrib.auth.models import User
from stdimage.models import StdImageField

class PostForm(forms.ModelForm):
    time = forms.TimeField(required = True, widget=forms.widgets.TimeInput)
    image = forms.ImageField(required = False)
    class Meta:
        model = Post
        fields = ('title','description', 'street_address', 'city', 'state', 'zip_code', 'date', 'time', 'price', 'image',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
	fields = ('about', 'college', 'year_in_school',)




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('entry',)

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


class EventCommentForm(forms.ModelForm):

    class Meta:
        model = EventComment
        fields = ('comment',)

class QuestionCommentForm(forms.ModelForm):

    class Meta:
        model = QuestionComment
        fields = ('comment',)

