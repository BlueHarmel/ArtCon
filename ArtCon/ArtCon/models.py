# from django.db import models


# class Member(models.Model):
#     name = models.CharField(max_length=10)
#     user_id = models.CharField(max_length=100)
#     pw = models.CharField(max_length=100)
#     email = models.EmailField()
#     number = models.PositiveBigIntegerField()


#     def __str__(self):
#         return str({'name': self.name,
#                     'user_id': self.user_id,
#                     'pw': self.pw,
#                     'email': self.email,
#                     'number': self.number,
#                     })

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

class exhibit(models.Model):
    E_name = models.CharField(200)
    L_name = models.CharField(50)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.CharField(100)
    fee = models.CharField(50)
    url = models.CharField(500)
    img = models.CharField(500)
    summary = models.CharField(1000)

    def __str__(self):
        return str({'E_name': self.E_name,
                    'L_name': self.L_name,
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'time': self.time,
                    'fee': self.fee,
                    'url': self.url,
                    'img': self.img,
                    'summary': self.summary
                    })

class location(models.Model):
    L_name = models.CharField(50)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return str({'L_name': self.L_name,
                    'x': self.x,
                    'y': self.y})

class CustomUser(AbstractUser):
    name = models.CharField(max_length=10)
    user_id = models.CharField(max_length=100)
    pw = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.PositiveBigIntegerField()


    def __str__(self):
        return str({'name': self.name,
                    'user_id': self.user_id,
                    'pw': self.pw,
                    'email': self.email,
                    'number': self.number,
                    })
    
class User(AbstractUser) :
    phone_number = PhoneNumberField(unique=True)
