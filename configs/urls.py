"""fcgurus_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('', include('escola.urls')),  # ESCOLA DIRETORIO PRINCIPAL
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('tutoriais/', include('tutoriais.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

