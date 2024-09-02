from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    tagList = models.TextField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)


