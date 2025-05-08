
from django.db import models
from django.contrib.auth.models import User

class UnpPoint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} のうんP: {self.point}うんP"

    def add_point(self, amount=1):
        self.point += amount
        self.save()
