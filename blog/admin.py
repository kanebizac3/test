from django.contrib import admin
from .models import Post, Comments, GasolineOwada, Category

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(GasolineOwada)
admin.site.register(Category)