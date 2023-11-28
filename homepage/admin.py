from django.contrib import admin

from homepage.models import Feedback, Notice

# Register your models here.
admin.site.register(Feedback)
admin.site.register(Notice)