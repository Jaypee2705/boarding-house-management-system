from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta
from django.db import models

# Create your models here.
class Tenant(models.Model):
    name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
    room = models.ForeignKey('boardinghouse.Room', on_delete=models.CASCADE, null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    add_month = models.DateField(null=True, blank=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name.get_full_name()

    def save(self, *args, **kwargs):
        if self.date_start != None and self.add_month == None:
            date_start = str(self.date_start)
            date_start = date_start.split('-')
            date_start = datetime(int(date_start[0]), int(date_start[1]), int(date_start[2]))
            self.add_month = date_start + relativedelta(months=1)
        super(Tenant, self).save(*args, **kwargs)


