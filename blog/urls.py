from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post/list', views.post_list, name='post_list'),
    path('', views.search_post, name='search_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('top', views.top, name='top'),
    path('top/life', views.life, name='life'),
    path('top/analytic', views.analytic, name='analytic'),
    path('policy', views.policy, name='policy'),
    path('term', views.term, name='term'),
    path('mission_promise', views.mission_promise, name="mission_promise"), 
    path('post/<int:post_id>/comment/<int:comment_id>/like/', views.like_post_view, name='like_post_url'),
    path('post/search', views.search_post, name='search_post'),
    path('map_view', views.map_view, name='map_view'),
    path('api/poi_sute_data/', views.get_poi_sute_data, name='get_poi_sute_data'),
    path('save_location/', views.save_location, name='save_location'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)