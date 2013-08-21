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

    # Messages details
    follow = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()

    def __unicode__(self):
        return self.name

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Messages(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.content
