from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.

class Cellphone_number (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cellphone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.cellphone_number