from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
class Boards(models.Model):
    boardName = models.CharField(max_length=20)
    description = models.TextField(max_length=100000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class List(models.Model):
    listTitle = models.CharField(max_length=200)
    board = models.ForeignKey(User, on_delete=models.CASCADE)

class Card(models.Model):
    cardTitle = models.CharField(max_length=200)
    cardDescription = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE,null=True)
    board = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
