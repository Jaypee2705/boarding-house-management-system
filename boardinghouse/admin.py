from django.contrib import admin

# Register your models here.

from .models import BoardingHouse, Room

admin.site.register(BoardingHouse)
admin.site.register(Room)