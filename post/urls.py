from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   
    path('', views.home,name="index"),
    path('bord/<bord_id>/',views.show,name='show'),
    path('topic/<int:topic_id>/post/create/', views.create_post, name='create_post'),
    path ('bord/<bord_id>/new',views.create,name='NewTobic'),
    path ('bord/<bord_id>/tobic/<tobic_id>',views.tobishow,name="tobishow"),
]
