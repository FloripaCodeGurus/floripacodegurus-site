from django.urls import path
from . import views

urlpatterns = [
    path('/profile/create/', views.profile_create, name='profile_create'),
    path('/profile/list/', views.profile_list, name='profile_list'),
    path('/profile/detail/', views.profile_detail, name='profile_detail'),


]