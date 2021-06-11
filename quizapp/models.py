from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime,date
from quiz.models import Question,Quiz
from members.models import User 
# Create your models here.
class Product(models.Model):
    
    question = models.CharField(max_length=200)
    option1 = models.TextField(blank=True, null=True)
    option2 = models.TextField(blank=True, null=True)
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)


class UserQuizData(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    q_category= models.ForeignKey(Quiz,on_delete=models.CASCADE)
    correct=models.BooleanField()
    wrong=models.BooleanField()

    def __str__(self):
        return str(self.user_id)+  ' | ' + str(self.question_id )
    
class userColloction(models.Model):
    # user_level=models.CharField(max_length=250,blank=True,null=True)
    user_p= models.ForeignKey(User,on_delete=models.CASCADE)
    user_points=models.IntegerField(blank=True,null=True,default=0)
    #level=models.IntegerField(blank=True,null=True)
    count = models.IntegerField(blank=True, default=0)
    attempts=models.IntegerField(blank=True,default=0)
    def __str__(self):
            return str(self.user_p)+  ' | ' + str(self.user_points )
    def total_likes(self):
        return self.user_points.count()
    # def save(self, *args, **kwargs):
    #     self.count = self.user_points.count()
    #     super(User, self).save(*args, **kwargs)