from django.contrib import admin

from payments.models import Bills, Payments, TransientPayment

# Register your models here.
admin.site.register(Bills)
admin.site.register(Payments)
admin.site.register(TransientPayment)