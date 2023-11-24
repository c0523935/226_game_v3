from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.board, name='board'),
    path('display/1/', views.display1, name='display1'),
    path('display/2/', views.display2, name='display2'),
    path('move_player/<str:player_id>/<str:direction>/', views.move_player, name='move_player'),
]
