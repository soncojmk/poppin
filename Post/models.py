from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

# Create your models here.

class Post(models.Model):
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


    #get_absolut_url method for easier urls
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])


