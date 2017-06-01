from django.conf.urls import *

from django.contrib import admin
from django.conf import settings
from activity_stream import views


urlpatterns = [

    #url(r'^$', 'activity_stream.views.feed', name='trending'),
                       # the three feed pages
    #url(r'^feed/$', 'activity_stream.views.feed', name=''),
    #url(r'^aggregated_feed/$', 'activity_stream.views.aggregated_feed', name='aggregated_feed'),
    #url(r'^notification_feed/$', 'activity_stream.views.notification_feed', name='notification_feed'),
                       # a page showing the users profile
    #url(r'^user/(?P<username>[\w_-]+)/$', 'activity_stream.views.profile', name='profile'),
                       # backends for follow and pin

    #url(r'^follow/$', 'activity_stream.views.follow', name='follow'),
    #url(r'^people/$', 'activity_stream.views.people', name='people'),


]
