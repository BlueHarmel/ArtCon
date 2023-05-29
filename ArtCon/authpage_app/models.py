from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User


    
class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
>>>>>>> abb19d86dc7d37f02cf4a0523411bf0b9aa3a566
