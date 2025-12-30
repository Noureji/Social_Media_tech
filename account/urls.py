from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
urlpatterns = [
   
    path('signup/', views.signup,name="signup"),
    path('logout/',auth_view.LogoutView.as_view(),name="logout"),
    path('login/' ,auth_view.LoginView.as_view(template_name='login.html'),name="login"),
    path('settings/changePas/',auth_view.PasswordChangeView.as_view(template_name='changePas.html'),name="changePas"),
    path('settings/password_change_done/',auth_view.PasswordChangeDoneView.as_view(template_name="done.html"),name='password_change_done')

]
