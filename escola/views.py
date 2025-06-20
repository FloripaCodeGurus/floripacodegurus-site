from django.shortcuts import render
from tutoriais.models import Tutoriais


def indice(request):
    tutoriais = Tutoriais.objects.all().order_by('-data_criacao')[:6]
    return render(request, 'escola/index.html', {'tutoriais': tutoriais})

def biopython(request):
    return render(request, 'escola/biopython.html', {})


def pythonmod1(request):
    return render(request, 'escola/python1.html', {})


def pythonmod2(request):
    return render(request, 'escola/python2.html', {})


def equipe(request):
    return render(request, 'escola/equipe.html', {})


def contato(request):
    return render(request, 'escola/contato.html', {})


def djangomodulo1(request):
    return render(request, 'escola/django1.html', {})