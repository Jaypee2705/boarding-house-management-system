from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from tenants.models import Tenant


class Bills(models.Model):
    room = models.ForeignKey('boardinghouse.Room', on_delete = models.CASCADE)
    bills = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)

    def __str__(self):
        return self.bills


class Payments(models.Model):
    room = models.ForeignKey('boardinghouse.Room', on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    mode = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.amount

    def save(self, *args, **kwargs):
        tenant = Tenant.objects.get(id=self.tenant.id)
        tenant.amount_paid = float(tenant.amount_paid) + float(self.amount)
        tenant.save()
        super(Payments, self).save(*args, **kwargs)