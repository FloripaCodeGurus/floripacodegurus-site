from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutoriais, name='tutoriais'),
    path('create/', views.tutorial_create, name='tutorial_create'),
    path('edit/<slug:slug>/', views.tutorial_edit, name='tutorial_edit'),
    # path('detail/<slug:slug>/', views.tutoriais_detalhe, name='tutoriais_detalhe'),
    path('detail/<slug:slug>/', views.tutoriais_detalhe, name='tutorial_detail'),
    path('delete/', views.tutorial_delete, name='tutorial_delete'),

]