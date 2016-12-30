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


class Blog(models.Model):

    MUSIC = '1'
    COMEDY = '2'
    FUNDRAISERS = '3'
    DANCE = '4'
    THEATRE = '5'
    IMPROV = '6'
    DEBATES = '7'
    ARTS = '8'
    CLUB_EVENT = '9'
    ACADEMIC = '10'
    PROFESSIONAL = '11'
    MOVIES = '12'

    CATEGORIES = (
    (MUSIC, 'Music'),
    (COMEDY, 'Comedy'),
    (FUNDRAISERS, 'Fundraisers'),
    (DANCE, 'Dance'),
    (THEATRE, 'Theatre'),
    (IMPROV, 'Improv'),
    (MOVIES, 'Movies'),
    (DEBATES, 'Debates'),
    (ARTS, 'Arts'),
    (CLUB_EVENT, 'Club Event'),
    (ACADEMIC, 'Academic'),
    (PROFESSIONAL, 'Professional'),
)

    category = models.CharField(max_length= 25, choices = CATEGORIES, null=True)
    title = models.CharField(max_length=32)
    description = models.TextField()
    image = StdImageField(upload_to='Post/images', null =True, blank=True,
                          variations={ 'large': {'width': 630, 'height': 300, 'crop': True}})

    video = models.URLField(null=True, blank=True)

    posted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)


