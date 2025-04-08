from django.conf import settings
from django.db import models
from django.utils import timezone
from django import forms
from django.core.validators import RegexValidator


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='img/', null=True, blank=True)  # 画像を保存するディレクトリを指定
    good = models.PositiveIntegerField(null=True, blank=True, verbose_name="評価")

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
