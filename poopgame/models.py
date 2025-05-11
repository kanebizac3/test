
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


class AttemptLog(models.Model):
    OPERATION_CHOICES = [
        ('add', '足し算'),
        ('sub', '引き算'),
        ('mul', '掛け算'),
        # ('div', '割り算') など必要に応じて追加
    ]

    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempt_logs')
    operation       = models.CharField(max_length=4, choices=OPERATION_CHOICES)
    operand_a       = models.PositiveSmallIntegerField()
    operand_b       = models.PositiveSmallIntegerField()
    user_answer     = models.IntegerField(null=True, blank=True)
    correct_answer  = models.IntegerField()
    is_correct      = models.BooleanField()
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.get_operation_display()} {self.operand_a},{self.operand_b} → {self.user_answer} ({'OK' if self.is_correct else 'NG'})"
    
from django.contrib.auth.models import User

class Chore(models.Model):
    """親が作るお手伝い項目"""
    name   = models.CharField("お手伝い内容", max_length=100)
    points = models.PositiveIntegerField("獲得ポイント", default=1)

    def __str__(self):
        return f"{self.name} ({self.points}P)"
