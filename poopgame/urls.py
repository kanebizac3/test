from django.urls import path
from . import views

urlpatterns = [
    path('programing', views.programing, name='poopgame_programing'),
    path('poopsub', views.poopsub, name='poopgame_poopsub'),
    path('multiply', views.multiply, name='multiply'),
    path('poopadd/', views.poopadd, name='poopadd'),
    path('poopadd/check/', views.poopadd_check, name='poopadd_check'),
    path('multiply2/', views.poopmultiply2, name='poopmultiply2'),
    path('multiply2/check/', views.poopmultiply2_check, name='poopmultiply2_check'),
    path('divide/',   views.divide,   name='divide'),
    path('home', views.home, name="home"),
]
