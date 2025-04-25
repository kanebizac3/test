from django.urls import path
from . import views

urlpatterns = [
    path('programing', views.programing, name='poopgame_programing'),
    path('poopsub', views.poopsub, name='poopgame_poopsub'),
    path('multiply', views.multiply, name='multiply'),

]
