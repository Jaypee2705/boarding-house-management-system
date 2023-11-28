from django.db import models

# Create your models here.
class Tenant(models.Model):
    name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
    room = models.ForeignKey('boardinghouse.Room', on_delete=models.CASCADE, null=True, blank=True)
    date_start = models.DateField()
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.name.get_full_name()


