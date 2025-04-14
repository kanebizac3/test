from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Map(models.Model):
    CATEGORY_CHOICES = [
        ('can', '空き缶'),
        ('bottle', 'ペットボトル'),
        ('glass', 'ビン'),
        ('snack', 'お菓子の袋'),
        ('other', 'その他'),
    ]

    latitude = models.FloatField()
    longitude = models.FloatField()
    reported_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='poisute_img/', null=True, blank=True)  # 画像を保存するディレクトリを指定
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_maps', null=True, blank=True)
    
    # 必要に応じて他のフィールド（ゴミの種類、写真など）を追加

    def __str__(self):
        return f"ポイ捨て報告 at ({self.latitude}, {self.longitude}) on {self.reported_at}"


# ---------ユーザーポイント機能--------
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def add_points(self, amount):
        self.points += amount
        self.save()

    def subtract_points(self, amount):
        if self.points >= amount:
            self.points -= amount
            self.save()
            return True
        return False

    class Meta:
        verbose_name = "ユーザープロフィール"
        verbose_name_plural = "ユーザープロフィール"