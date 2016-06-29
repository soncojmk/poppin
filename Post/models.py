from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    class Meta:
       verbose_name_plural='Categories'

    def __unicode__(self):
        return self.name


class Post(models.Model):
    category = models.ManyToManyField(Category)
    author = models.ForeignKey('auth.user')
    title = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)
    date = models.DateField(default='', null=True)
    time = models.TimeField(blank=True, null=True)
    description = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField(upload_to="Post/images/", null=True, blank=True)
    posted_date = models.DateTimeField(default=timezone.now)

    tags = TaggableManager()
    
    
    def posted(self):
        self.posted_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    #get_absolut_url method for easier urls
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])

class Question(models.Model):
    author = models.ForeignKey('auth.user')
    entry = models.TextField(max_length=200, blank=True, null=True, verbose_name="")
    posted_date = models.DateTimeField(default=timezone.now)

    def posted(self):
        self.posted_date=timezone.now()
        self.save()

    def __str__(self):
        return self.entry

    def approved_comments(self):
        return self.questioncomments.filter(approved_comment=True)

    #get_absolut_url method for easier urls
    def get_absolute_url(self):
        return reverse('question_detail', args=[self.pk])
   
    class Meta:
        verbose_name_plural='questions'
        
    
class EventComment(models.Model):
    post = models.ForeignKey('Post.Post', related_name='comments')
    author = models.ForeignKey('auth.user')
    comment = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.comment
    


class QuestionComment(models.Model):
    question = models.ForeignKey('Post.Question', related_name='questioncomments')
    author = models.ForeignKey('auth.user')
    comment = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.comment

 







