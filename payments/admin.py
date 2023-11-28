from django.contrib import admin

from payments.models import Bills, Payments

# Register your models here.
admin.site.register(Bills)
admin.site.register(Payments)