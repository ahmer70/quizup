from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio=models.TextField(max_length=250, blank=True)
    profile_pic=models.ImageField(blank=True,null=True,upload_to="images/profile/",default="pic.jpg")
    country=models.CharField(max_length=250,blank=True,null=True)
    def getImage(self):
        if not self.image:
            # depending on your template
            return 'media/pic.jpg' 