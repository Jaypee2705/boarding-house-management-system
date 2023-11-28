from django.db import models

from boardinghouse.models import Room


class Bills(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bills = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)

    def __str__(self):
        return self.bills
