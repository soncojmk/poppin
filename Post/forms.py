from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, EventComment, Question, QuestionComment, Concert, ConcertComment, Survey, Broadcast_Email
from haystack.forms import SearchForm

from taggit_labels.widgets import LabelWidget
from taggit.forms import *
from taggit.models import Tag
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django.forms.extras.widgets import SelectDateWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'



class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('name', 'email', 'description',)


class BroadCastForm(forms.ModelForm):
    class Meta:
        model = Broadcast_Email
        fields = ('subject', 'text_content', 'html_content',)



class PostForm(forms.ModelForm):
   # date = forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    #time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'placeholder': '24 hour clock only'}))

    image = forms.ImageField(required = False)
    class Meta:
        model = Post
        fields = ('category', 'title','description', 'street_address', 'city', 'state', 'zip_code', 'date', 'time', 'price', 'ticket_link', 'image',)
        widgets = {
            'price': forms.NumberInput(attrs={'placeholder': 'Price in dollars'}),
            'description': forms.Textarea(),
            'date': SelectDateWidget,
            'end_date': SelectDateWidget,
            'time': TimeInput(),
            'ticket_link': forms.TextInput(attrs={'placeholder': 'optional'})


            #'date': DateWidget(usel10n=True, bootstrap_version=3),
            #'time': TimeWidget(usel10n=True, bootstrap_version=3)
        }
'''
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
	fields = ('about', 'college', 'year_in_school',)
'''



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('entry',)



class ConcertForm(forms.ModelForm):
    #date = forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    #time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'placeholder': '24 hour clock only'}))

    image = forms.ImageField(required = False)
    class Meta:
        model = Concert
        fields = ('title','description', 'street_address', 'city', 'state', 'zip_code', 'date', 'time', 'ticket_link', 'starting_price', 'image',)
        widgets = {
            'description': forms.Textarea(),
            'date': SelectDateWidget,
            'time': TimeInput()

            #'date': DateWidget(usel10n=True, bootstrap_version=3),
            #'time': TimeWidget(usel10n=True, bootstrap_version=3)
        }


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

class ConcertCommentForm(forms.ModelForm):

    class Meta:
        model = ConcertComment
        fields = ('comment',)

