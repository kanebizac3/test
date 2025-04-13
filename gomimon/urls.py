from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('map', views.map, name='map'),
    # path('gomimon', views.gomimon, name='gomimon'),
    path('test', views.test, name='test'),
    path('api/map_data/', views.get_map_data, name='get_map_data'),
    path('save_location/', views.save_location, name='save_location'),  # 他のURLパターン
    path('submit_map_data/', views.submit_map_data, name='submit_map_data'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)