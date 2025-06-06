from django.conf import settings
from django.db import models
from django.utils import timezone
from django import forms
from django.core.validators import RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='img/', null=True, blank=True)  # 画像を保存するディレクトリを指定
    good = models.PositiveIntegerField(null=True, blank=True, verbose_name="評価")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
# comments

class Comments(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='img/', null=True, blank=True)  # 画像を保存するディレクトリを指定
    good = models.PositiveIntegerField(null=True, blank=True, verbose_name="評価")

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
    

class GasolineOwada(models.Model):
    regular = models.CharField(max_length=3,
        validators=[RegexValidator(r'^\d{3}$', message='3桁の数字')],
                    verbose_name='レギュラー',
    )
    deisel = models.CharField(max_length=3,
        validators=[RegexValidator(r'^\d{3}$', message='3桁の数字')],
                    verbose_name='軽油',
    )
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return "Owada"


from django.db import models
from django.utils import timezone

class PoiSute(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    reported_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='poisute_img/', null=True, blank=True)  # 画像を保存するディレクトリを指定
    category = models.CharField(max_length=100, null=True, blank=True)
    
    # 必要に応じて他のフィールド（ゴミの種類、写真など）を追加

    def __str__(self):
        return f"ポイ捨て報告 at ({self.latitude}, {self.longitude}) on {self.reported_at}"