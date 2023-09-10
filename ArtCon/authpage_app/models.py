from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from exhibpage_app.models import Performance

# from django.contrib.auth.models import User


class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    followed_perform = models.ManyToManyField(Performance, related_name="followers")
    birth = models.DateField()
    gender = models.SmallIntegerField()
    # prefer_title = models.CharField(max_length=200, null=True)
