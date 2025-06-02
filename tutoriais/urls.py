from django.urls import path
from django.urls import path
from . import views
urlpatterns = [
    path('',views.tutoriais, name='tutoriais'),
    path('page2/',views.tutoriais2, name='tutoriais2'),
    path('bio001/',views.bio001, name='bio001'),
    path('currencylayer/',views.currencylayer, name='currencylayer'),
    path('histogramas/',views.histogramas, name='histogramas'),
    path('regex/',views.regex, name='regex'),
    path('lista/', views.tutoriais_lista, name='tutoriais_lista'),
    path('<slug:slug>/', views.tutoriais_detalhe, name='tutoriais_detalhe'),

]
