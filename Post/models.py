from __future__ import unicode_literals
#from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from geopy.geocoders import GoogleV3
#from geopy.geocoders.google import GQueryError
from urllib2 import URLError

from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField
from stdimage.models import StdImageField

from stream_django import activity
from stream_django.feed_manager import feed_manager
from django.db.models import signals
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import F


# Create your models here.



class Survey(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    description = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def posted(self):
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return self.email

#events model/ main model
class Post(activity.Activity, models.Model):

    MUSIC = '1'
    SPORTS = '2'
    FUNDRAISERS = '3'
    DANCE = '4'
    PERFORMING_ARTS = '6'
    THEATRE = '5'
    ARTS = '7'
    ART = '8'
    CLUB_EVENT = '9'
    ACADEMIC = '10'
    PROFESSIONAL = '11'
    MOVIES = '12'
    COMEDY = '13'
    POETRY = '14'
    OTHER = '15'
    WP = '16'
    LECTURE = '17'
    DEBATE = '18'
    HEALTH ='19'
    GAMING ='20'
    POLITICAL ='21'

    CATEGORIES = (
    (MUSIC, 'Music'),
    (FUNDRAISERS, 'Fundraisers'),
    (COMEDY, 'Comedy'),
    (POETRY, 'Poetry'),
    (DANCE, 'Dance'),
    (HEALTH, 'Health/Wellbeing'),
    (THEATRE, 'Theatre'),
    (ART, 'Art'),
    (MOVIES, 'Films'),
    (PERFORMING_ARTS, 'Performing Arts'),
    (SPORTS, 'Sports'),
    (POLITICAL, 'Political'),
    (DEBATE, 'Debate'),
    (GAMING, 'Gaming'),
    (LECTURE, 'Lecture'),
    (ACADEMIC, 'Academic'),
    (PROFESSIONAL, 'Professional'),
    (OTHER, 'Other'),
)

    category = models.CharField(max_length= 25, choices = CATEGORIES, null=True)
    author = models.ForeignKey('auth.user')
    title = models.CharField(max_length=32)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=64)
    state = USStateField(choices = STATE_CHOICES)
    zip_code = models.CharField(max_length=5)
    date = models.DateField(help_text= "MM/DD/YYYY", null=True)

    end_date = models.DateField(help_text="not requiered", blank=True, null=True)

    time = models.TimeField( help_text="24 hour clock", null=True,)
    description = models.TextField()
    price = models.IntegerField(null=True)
    ticket_link = models.URLField(null=True, blank=True)
    image = StdImageField(upload_to='Post/images', null =True, blank=True,
                          variations={ 'large': {'width': 630, 'height': 300, 'crop': True}})

    posted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    country = "United States"

    draft = models.BooleanField(default=False)

    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)

    saves = models.IntegerField(null=True)

    gis = gis_models.GeoManager()
    objects = models.Manager()
    #draft = models.BooleanField(default=False)
    #tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-posted_date']

    def posted(self):
        self.posted_date=timezone.now()
        self.save()


    @property
    def time_since(self):
        return (timezone.now()-self.posted_date).total_seconds()

    @property
    def activity_actor_attr(self):
        return self.author


    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'{c}/{l}/{p}'.format(c=self.title, l=self.description, p=self.author)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    #get_absolut_url method for easier urls
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])

    '''
    def save(self, **kwargs):
        if not self.location:
            address = u'%s %s' % (self.city, self.street_address)
            address = address.encode('utf-8')
            geocoder = GoogleV3()
            try:
                _, latlon = geocoder.geocode(address)
            except (URLError, ValueError):
                latlon = None
                pass
            else:
                point = "POINT(%s %s)" % (latlon[0], latlon[1])
                self.location = geos.fromstr(point)
        super(Post, self).save()
    '''

class Question(activity.Activity, models.Model):
    author = models.ForeignKey('auth.user')
    entry = models.TextField(max_length=200, blank=False, null=True, verbose_name="")
    posted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def posted(self):
        self.posted_date=timezone.now()
        self.save()


    def time_since(self):
        return (timezone.now()-self.posted_date).total_seconds()

    @property
    def activity_actor_attr(self):
        return self

    def __str__(self):
        return self.entry

    def approved_comments(self):
        return self.questioncomments.filter(approved_comment=True)

    #get_absolut_url method for easier urls
    def get_absolute_url(self):
        return reverse('question_detail', args=[self.pk])

    class Meta:
        verbose_name_plural='questions'


class Concert(activity.Activity, models.Model):
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
    ticket_link = models.URLField()
    starting_price = models.IntegerField(null=True)
    image = StdImageField(upload_to='Post/images', null =True, blank=True,
                          variations={ 'large': {'width': 630, 'height': 300, 'crop': True}})

    posted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    #tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def posted(self):
        self.posted_date=timezone.now()
        self.save()


    @property
    def time_since(self):
        return (timezone.now()-self.posted_date).total_seconds()


    @property
    def activity_actor_attr(self):
        return self.author


    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'{c}/{l}/{p}'.format(c=self.title, l=self.description, p=self.author)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    #get_absolut_url method for easier urls
    def get_absolute_url(self):
        return reverse('concert_detail', args=[self.pk])



class ConcertComment(activity.Activity, models.Model):
    concert = models.ForeignKey('Post.Concert', related_name='concertcomments', default="")
    author = models.ForeignKey('auth.user')
    comment = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    approved_comment = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    @property
    def activity_actor_attr(self):
        return self

    def __str__(self):
        return self.comment


class EventComment(activity.Activity, models.Model):
    post = models.ForeignKey('Post.Post', related_name='comments')
    author = models.ForeignKey('auth.user')
    comment = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    approved_comment = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    @property
    def activity_actor_attr(self):
        return self

    def __str__(self):
        return self.comment



class QuestionComment(activity.Activity, models.Model):
    question = models.ForeignKey('Post.Question', related_name='questioncomments')
    author = models.ForeignKey('auth.user')
    comment = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    approved_comment = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    @property
    def activity_actor_attr(self):
        return self

    def __str__(self):
        return self.comment




class Broadcast_Email(models.Model):
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)

    html_content = models.TextField(null=True, default=None)
    text_content = models.TextField(null=True, default=None)

    def __unicode__(self):
        return self.subject




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









