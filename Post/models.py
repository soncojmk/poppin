from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField
from stdimage.models import StdImageField

# Create your models here.
'''
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    class Meta:
       verbose_name_plural='Categories'

    def __unicode__(self):
        return self.name
'''


class Post(models.Model):
    #category = models.ManyToManyField(Category)
    author = models.ForeignKey('auth.user')
    title = models.CharField(max_length=32)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=64)
    state = USStateField(choices = STATE_CHOICES)
    zip_code = models.CharField(max_length=5)
    date = models.DateField(help_text= "MM/DD/YYYY", blank=True, null=True)
    time = models.TimeField( help_text="24 hour clock", blank=True, null=True,)
    description = models.TextField()
    price = models.IntegerField()
    image = StdImageField(upload_to='Post/images', null =True, blank=True,
                          variations={ 'large': {'width': 630, 'height': 300, 'crop': True}})

    posted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    #tags = TaggableManager()


    def posted(self):
        self.posted_date=timezone.now()
        self.save()


    @property
    def time_since(self):
        return (timezone.now()-self.posted_date).total_seconds()


    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    #get_absolut_url method for easier urls
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])

class Question(models.Model):
    author = models.ForeignKey('auth.user')
    entry = models.TextField(max_length=200, blank=False, null=True, verbose_name="")
    posted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def posted(self):
        self.posted_date=timezone.now()
        self.save()


    def time_since(self):
        return (timezone.now()-self.posted_date).total_seconds()

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
    created_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
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
    created_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.comment

'''
class Profile(models.Model):
    user = models.ForeignKey('auth.user', unique=True)
    about = models.TextField(help_text="tell us about your shitty professors or something")
    college = models.CharField(max_length=50)

    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'

    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_school = models.CharField(
        max_length=10,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

'''









