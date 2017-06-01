from __future__ import unicode_literals

from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
class Ticket(models.Model):
	email = models.CharField(max_length=128, unique=False)
	confirmation_num = models.CharField(max_length=20, primary_key=True, unique=True)
	event_name = models.CharField(max_length=128, unique = False)
	confirmed = models.CharField(max_length=20, unique=False)

	def __unicode__(self):
		return self.confirmation_num
