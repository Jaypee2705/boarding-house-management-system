from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Custom_User(AbstractUser):
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)