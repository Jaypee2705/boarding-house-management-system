from django.db import models

# Create your models here.

class Feedback(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.get_full_name()