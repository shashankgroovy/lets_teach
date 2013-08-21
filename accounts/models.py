import hashlib

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # General details
    user = models.OneToOneField(User)

    # Personal details
    gender = models.CharField(max_length=7)
    birthday = models.DateField()
    city = models.CharField(max_length=100)

    # Professional details
    college = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    college_major = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

    # Teaching details
    subject = models.CharField(max_length=100)

    # Outloud details
    follow = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()

    def __unicode__(self):
        return self.name

