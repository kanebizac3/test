# poopgame/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import UnpPoint


# 標準の User モデルをそのまま使用（カスタムユーザーを使わない場合）
admin.site.unregister(User)
admin.site.register(UnpPoint)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'date_joined')
    search_fields = ('username',)
