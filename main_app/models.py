from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    profile_name = models.CharField(max_length=15)
    bio = models.TextField(max_length=250)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.profile_name

class Post(models.Model):
    content = models.TextField(max_length=256)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)