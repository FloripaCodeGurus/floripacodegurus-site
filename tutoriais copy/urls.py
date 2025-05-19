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

]
