from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
#from stream_django.activity import Activity
#from stream_django.feed_manager import feed_manager

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True



class Follow(BaseModel):
    '''
    A simple table mapping who a user is following.
    For example, if user is Kyle and Kyle is following Alex,
    the target would be Alex.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='following_set')
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='follower_set')
'''
    @classmethod
    def activity_related_models(cls):
        return ['user', 'target']

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_notify(self):
       # target_feed = feed_manager.get_notification_feed(self.target_id)
        return #[target_feed]


def follow_change(sender, instance, created, **kwargs):
    if instance.deleted_at is None:
        #feed_manager.follow_user(instance.user_id, instance.target_id)
    else:
        

#feed_manager.unfollow_user(instance.user_id, instance.target_id)

	
def unfollow_feed(sender, instance, **kwargs):
    #feed_manager.unfollow_user(instance.user_id, instance.target_id)


post_save.connect(follow_change, sender=Follow)
post_delete.connect(unfollow_feed, sender=Follow)

'''
