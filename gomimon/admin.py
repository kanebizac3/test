
from django.contrib import admin
from .models import Map, UserProfile, Egg, UserGomimon, Gomimon

admin.site.register(Map)
admin.site.register(UserProfile)
admin.site.register(Egg)
admin.site.register(UserGomimon)
# admin.site.register(Gomimon)

class GomimonAdmin(admin.ModelAdmin):
    list_display = ('name', 'gomimon_type', 'hp', 'attack', 'defense') # 一覧表示するフィールド
    search_fields = ('name',) # 検索対象とするフィールド
    # 他のAdmin設定 (filter, ordering など) もここに追加できます

admin.site.register(Gomimon, GomimonAdmin)