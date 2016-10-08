import datetime
from haystack import indexes
from Post.models import Post, Question, Concert
from django.contrib.auth.models import User
from account.models import Account

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author')
    posted_date = indexes.DateTimeField(model_attr='posted_date')
    price = indexes.IntegerField(model_attr='price')
    #date = indexes.DateField(model_attr='date')  creates error


    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #entry = indexes.TextField(model_attr='')
    author = indexes.CharField(model_attr='author')
    posted_date = indexes.DateTimeField(model_attr='posted_date')
    #date = indexes.DateField(model_attr='date')  creates error


    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class ConcertIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author')
    posted_date = indexes.DateTimeField(model_attr='posted_date')
    #date = indexes.DateField(model_attr='date')  creates error


    def get_model(self):
        return Concert

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #username = indexes.CharField(model_attr='username')
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')


    def get_model(self):
        return User

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class AccountIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
   # user = indexes.CharField(model_attr='User')


    def get_model(self):
	return Account

    def index_queryset(self, using=None):
	"""Used when the entire index for model is updated."""
	return self.get_model().objects.all()
