from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Account(models.Model):
    # General details
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    # Personal details
    #birthday = models.DateField()
    city = models.CharField(max_length=100)

    # Professional details
    currentedu = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    college_major = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

    # Teaching details
    # choose the subjects one would like to teach
    # science, maths, english, if other then specify

    def __unicode__(self):
        return self.name

# create our user object to attach to our account object
def create_account_user_callback(sender, instance, **kwargs):
    account.new = Account.objects.get_or_create(user=instance)
post_save.connect(create_account_user_callback, User)
