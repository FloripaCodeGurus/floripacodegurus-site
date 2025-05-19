from django.urls import path
from . import views
urlpatterns = [
    path('',views.indice, name='indice'),
    path('biopython_mod1/',views.biopython, name='biopython'),
    path('python_mod1/',views.pythonmod1, name='pythonmodulo1'),
    path('python_mod2/',views.pythonmod2, name='pythonmodulo2'),
    path('django_mod1/', views.djangomodulo1, name='djangomodulo1'),
    path('equipe/',views.equipe, name='equipe'),
    path('contato/',views.contato, name='contato'),

]
