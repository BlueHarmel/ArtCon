from django.db import models
from authpage_app.models import User
import datetime
# Create your models here.

class Post(models.Model):
    postname = models.CharField(max_length=50)
    contents = models.CharField(max_length=500)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(datetime.datetime.now())

    def __str__(self):
        return str({'postname' : self.postname,
                    'contents' : self.contents,
                    'username' : self.username,
                    'date' : self.date})
    
class Comment(models.Model):
    contents = models.CharField(max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(datetime.datetime.now())