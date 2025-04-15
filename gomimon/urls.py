from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('map', views.map, name='map'),
    # path('gomimon', views.gomimon, name='gomimon'),
    path('test', views.test, name='test'),
    path('api/map_data/', views.get_map_data, name='get_map_data'),
    path('save_location/', views.save_location, name='save_location'),  # 他のURLパターン
    path('submit_map_data/', views.submit_map_data, name='submit_map_data'),
    path('register/', views.register, name='register'),
    path('register/success/', views.registration_success, name='registration_success'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('gomimon', views.gomimon, name='gomimon'),
    path('buy_egg/', views.buy_egg, name='buy_egg'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)