from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('top', views.top, name='top'),
    path('top/life', views.life, name='life'),
    path('top/analytic', views.analytic, name='analytic'),
    path('policy', views.policy, name='policy'),
    path('term', views.term, name='term'),
    path('mission_promise', views.mission_promise, name="mission_promise"),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)