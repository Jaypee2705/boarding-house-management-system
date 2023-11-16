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
    # owner = models.ForeignKey('auth.User', related_name='boardinghouses', on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Room(models.Model):
    boardinghouse = models.ForeignKey(BoardingHouse, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_bed = models.IntegerField()

    male_female_choices = (
        ("For Male Only", "For Male Only"),
        ("For Female Only", "For Female Only"),
        ("For Both Male and Female", "For Both Male and Female")
    )
    male_female = models.CharField(choices=male_female_choices, max_length=50)
    vacant = models.BooleanField(default=True)
    image = models.ImageField(upload_to='room', blank=True)


    def __str__(self):
        return self.name