from django.db import models

# Create your models here.
class Tenant(models.Model):
    name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    room = models.ForeignKey('boardinghouse.Room', on_delete=models.CASCADE, null=True, blank=True)


