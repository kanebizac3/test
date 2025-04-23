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
    STATUS_CHOICES = [("picked", "回収済み"),
              ("not_picked", "未回収")]

    latitude = models.FloatField()
    longitude = models.FloatField()
    reported_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='poisute_img/', null=True)  # 画像を保存するディレクトリを指定
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_maps', null=True, blank=True)
    picking = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    good = models.IntegerField(default=0, null=True, blank=True)
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

class Egg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eggs')
    created_at = models.DateTimeField(auto_now_add=True)
    # 卵の種類、ステータスなど、必要に応じてフィールドを追加
    # 例: name = models.CharField(max_length=100)

class UserGomimon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gomimon_name = models.CharField(max_length=100)
    gomimon_image = models.CharField(max_length=100)
    gomimon_level = models.IntegerField(null=True)
    gomimon_atack = models.IntegerField(null=True)
    gomimon_defence = models.IntegerField(null=True)
    gomimon_maxhp = models.IntegerField(null=True)
    gomimon_hp = models.IntegerField(null=True)
    gomimon_element = models.CharField(default="ノーマル", max_length=10, null=True)
    gomimon_skill = models.CharField(max_length=30, blank=True, null=True)
    gomimon_exp = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gomimon_name} (オーナー: {self.user.username})"
    
class GomimonType(models.TextChoices):
    BURNABLE = 'burnable', '燃えるゴミ'
    NONBURNABLE = 'nonburnable', '燃えないゴミ'
    CAN = 'can', '資源ごみ（缶）'
    PET = 'pet', '資源ごみ（ペット）'
    BIN = 'bin', '資源ごみ（びん）'
    PLASTIC = 'plastic', 'プラスチック'
    PAPER = 'paper', '資源ごみ（紙類）'
    BIG = "big",  '粗大ゴミ'
    TOXIC = "toxic", "有害ゴミ"
    DARK = "dark", "闇"  #敵の属性
    
class Gomimon(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='gomimon_images/', blank=True)
    gomimon_type = models.CharField(max_length=20, choices=GomimonType.choices)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    skill = models.CharField(max_length=100)
    skill_effect = models.TextField(blank=True)