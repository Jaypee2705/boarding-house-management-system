from django.db import models

# Create your models here.

class Feedback(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)


    def __str__(self):
        return self.user.get_full_name()


class Notice(models.Model):
    title = models.CharField(max_length=100)
    notice = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    boardinghouse = models.ForeignKey('boardinghouse.BoardingHouse', on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return self.title