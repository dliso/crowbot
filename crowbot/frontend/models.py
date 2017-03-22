from django.db import models
#from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

class UserQuery(models.Model):
    query_text = models.CharField(max_length=500)

    def __str__(self):
        return self.query_text[:50]


