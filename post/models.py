from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Board(models.Model):
   
    name=models.CharField(max_length=40,unique=True)
    description =models.CharField(max_length=120 )

class Topic(models.Model):
    
    subject=models.CharField()
    bord=models.ForeignKey(Board,related_name='topics',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='topics',on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    
    message=models.TextField()
    topic = models.ForeignKey(Topic ,related_name='posts',on_delete=models.CASCADE)
    created_by =models.ForeignKey(User,related_name='Posts',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.topic} {self.message}"