# from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from backend import models as backend_models

from api.usertype import *


# Create your models here.
# @python_2_unicode_compatible

class Profile(models.Model):
    STUDENT = 1
    PROFESSOR = 2
    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    )
    #Dette er modellen for formen i admin viewet.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=30, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    subscribed_courses = models.ManyToManyField(backend_models.Course)

    def __str__(self):
        return self.user.username

    def to_dict(self):
        usertype = USERTYPE.from_profile_role(self.role)
        return {
            'name': self.user.first_name,
            'pk': self.user.id,
            'usertype': usertype,
            'avatarUrl': '',
        }

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()#lagrer dataen som profilen får inn
