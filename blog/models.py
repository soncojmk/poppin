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

#from stream_django import activity
#from stream_django.feed_manager import feed_manager
from django.db.models import signals
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import F


class Blog(models.Model):

    author = models.ForeignKey('auth.user', default="")
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = StdImageField(upload_to='Post/images', null =True, blank=True,
                          variations={ 'large': {'width': 630, 'height': 300, 'crop': True}})

    #video = models.URLField(null=True, blank=True)

    posted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        ordering = ['-posted_date']

    def posted(self):
        self.posted_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'{c}/{l}'.format(c=self.title, l=self.description)

