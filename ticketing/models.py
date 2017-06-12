from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Ticket(models.Model):
    event_id = models.IntegerField()