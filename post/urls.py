from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="index"),

    path('bord/<int:bord_id>/', views.show, name='show'),
    path('bord/<int:bord_id>/new/', views.create, name='NewTobic'),
    path('bord/<int:bord_id>/tobic/<int:tobic_id>/', views.tobishow, name="tobishow"),
    
    path('board/<int:id>/delete/', views.board_delete, name='board_delete'),
    path('topic/<int:topic_id>/post/create/', views.create_post, name='create_post'),

    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
]
