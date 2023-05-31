from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User


    
class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    prefer_title = models.CharField(max_length=200)