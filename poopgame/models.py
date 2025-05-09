
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
        # ポイント履歴を残す
        UnpPointHistory.objects.create(user=self.user, points=amount)


class UnpPointHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unp_history')
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 週間ランキング集計のため、timestampでソートしても良い
        ordering = ['-timestamp']
