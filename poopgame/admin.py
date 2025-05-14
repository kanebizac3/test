# poopgame/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import UnpPoint, UnpPointHistory, Chore


# 標準の User モデルをそのまま使用（カスタムユーザーを使わない場合）
admin.site.unregister(User)
admin.site.register(UnpPoint)
admin.site.register(UnpPointHistory)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'date_joined')
    search_fields = ('username',)

from .models import AttemptLog

@admin.register(AttemptLog)
class AttemptLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'operation', 'operand_a', 'operand_b', 'user_answer', 'correct_answer', 'is_correct', 'timestamp')
    list_filter  = ('operation', 'is_correct', 'timestamp')
    search_fields= ('user__username',)



@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display   = ('user', 'name', 'points')
    list_filter    = ('user',)
    search_fields  = ('name', 'user__username')

from django.contrib import admin
from .models import ShopItem, PurchaseRequest

admin.site.register(ShopItem)
admin.site.register(PurchaseRequest)