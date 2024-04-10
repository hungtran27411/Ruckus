from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    profile_name = models.CharField(max_length=15)
    bio = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
    content = models.TextField(max_length=256)