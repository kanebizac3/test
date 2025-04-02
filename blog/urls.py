from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('top', views.top, name='top'),
    path('top/life', views.life, name='life'),
    path('top/analytic', views.analytic, name='analytic'),

]