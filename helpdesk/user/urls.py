
from django.urls import path, include
from django.contrib.auth import admin
from .views import signup_view, login_view, logout_view

urlpatterns = [
    path('login/', login_view,  name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/',  signup_view, name='signup'),
]