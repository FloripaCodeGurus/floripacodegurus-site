from django.urls import path
from . import views

urlpatterns = [
    path("inscricao/", views.inscrever, name="inscricao"),
]