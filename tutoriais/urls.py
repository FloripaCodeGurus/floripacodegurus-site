from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutoriais, name='tutoriais'),
    # path('page2/', views.tutoriais2, name='tutoriais2'),
    # path('bio001/', views.bio001, name='bio001'),
    # path('currencylayer/', views.currencylayer, name='currencylayer'),
    # path('histogramas/', views.histogramas, name='histogramas'),
    # path('regex/', views.regex, name='regex'),
    path('list/', views.tutorial_list, name='tutorial_list'),
    path('create/', views.tutorial_create, name='tutorial_create'),
    path('detail/<slug:slug>/', views.tutorial_detail, name='tutorial_detail'),
]