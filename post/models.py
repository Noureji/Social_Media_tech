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
    

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} likes post {self.post.id}"

class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.id}"