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
    path('register/', views.register, name='gomimon_register'),
    path('register/success/', views.registration_success, name='registration_success'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='gomimon_login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('gomimon', views.gomimon, name='gomimon'),
    path('buy_egg/', views.buy_egg, name='buy_egg'),
    path('battle/', views.start_battle_view, name='start_battle'),
    path('battle/next_turn/', views.next_turn_view, name='next_turn'),
    path('hatch/', views.hatch_gomimon, name='hatch_gomimon'),
    path('error/', views.gomimon, name='error'),
    path('release_gomimon/', views.release_gomimon, name='release_gomimon'),
    path('secret/create_gomimon/', views.create_gomimon, name='create_gomimon'),
    path('heal_gomimon/', views.heal_gomimon, name='heal_gomimon'),
    path('api/good/<int:report_id>/', views.good_report, name='good_report'),
    path('logout/', auth_views.LogoutView.as_view(next_page='map'), name='gomimon_logout'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)