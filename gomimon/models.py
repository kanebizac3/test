
from django.db import models
from django.utils import timezone

class Map(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    reported_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='poisute_img/', null=True, blank=True)  # 画像を保存するディレクトリを指定
    category = models.CharField(max_length=100, null=True, blank=True)
    
    # 必要に応じて他のフィールド（ゴミの種類、写真など）を追加

    def __str__(self):
        return f"ポイ捨て報告 at ({self.latitude}, {self.longitude}) on {self.reported_at}"