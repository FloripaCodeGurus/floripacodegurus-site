from django.shortcuts import render, get_object_or_404
from .models import Tutoriais


def tutoriais(request):
    return render(request, 'tutoriais/tutoriais.html', {})


def tutoriais2(request):
    return render(request, 'tutoriais/tutoriais2.html', {})


def currencylayer(request):
    return render(request, 'tutoriais/currency.html', {})


def histogramas(request):
    return render(request, 'tutoriais/histogramas.html', {})


def regex(request):
    return render(request, 'tutoriais/regex.html', {})


def bio001(request):
    return render(request, 'tutoriais/bio_001.html', {})


def tutoriais_lista(request):
    tutoriais = Tutoriais.objects.all().order_by('-data_criacao')
    return render(request, 'tutoriais/lista_tutoriais.html', {'tutoriais': tutoriais})


def tutoriais_detalhe(request, slug):
    tutorial = get_object_or_404(Tutoriais, slug=slug)
    return render(request, 'tutoriais/tutoriais_detalhe.html', {'tutorial': tutorial})
                                                              

                                                            