from django.shortcuts import render


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