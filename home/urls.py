from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/',views.home, name='home-home'),
    #path('',views.login, name='home-login'),
    path('about/',views.about, name='home-about'),
    path('',auth_views.LoginView.as_view(template_name='home/login.html'),name='home-login')
]
