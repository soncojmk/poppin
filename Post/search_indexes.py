import datetime
from haystack import indexes
from Post.models import Post, Question

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author')
    posted_date = indexes.DateTimeField(model_attr='posted_date')
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
