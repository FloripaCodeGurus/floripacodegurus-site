from django.shortcuts import render


def indice(request):
    return render(request, 'escola/index.html', {})

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