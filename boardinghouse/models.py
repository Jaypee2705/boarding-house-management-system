from django.db import models

# Create your models here.

class BoardingHouse(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    address = models.CharField(max_length=100)
    num_beds = models.IntegerField()
    num_baths = models.IntegerField()
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    image = models.ImageField(upload_to='boardinghouse', blank=True)
    owner = models.ForeignKey('auth.User', related_name='boardinghouses', on_delete=models.CASCADE)

    def __str__(self):
        return self.name



