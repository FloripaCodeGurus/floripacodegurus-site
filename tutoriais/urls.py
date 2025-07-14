from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutoriais, name='tutoriais'),
    # path('page2/', views.tutoriais2, name='tutoriais2'),
    # path('bio001/', views.bio001, name='bio001'),
    # path('currencylayer/', views.currencylayer, name='currencylayer'),
    # path('histogramas/', views.histogramas, name='histogramas'),
    # path('regex/', views.regex, name='regex'),
    path('create/', views.tutorial_create, name='tutorial_create'),
    path('edit/<slug:slug>/', views.tutorial_edit, name='tutorial_edit'),
    path('lista/', views.tutoriais_lista, name='tutoriais_lista'),
    path('detail/<slug:slug>/', views.tutoriais_detalhe, name='tutoriais_detalhe'),
    path('delete/', views.tutorial_delete, name='tutorial_delete'),

]