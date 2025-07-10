from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Tutoriais


def tutoriais(request):
    tutoriais = Tutoriais.objects.all().order_by('-data_criacao')
    return render(request, 'tutoriais/tutoriais.html', {'tutoriais': tutoriais})


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


def tutorial_create(request):
    if request.method == 'POST':
        tutorial = Tutoriais(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            introducao=request.POST.get('introducao'),
            conceitos=request.POST.get('conceitos'),
            exemplos=request.POST.get('exemplos'),
            conclusao=request.POST.get('conclusao'),
            autor=request.POST.get('autor'),
            categoria=request.POST.get('categoria'),
            nivel=request.POST.get('nivel')
        )
        if request.FILES.get('imagem'):
            tutorial.imagem = request.FILES['imagem']
        tutorial.save()
        messages.success(request, 'Tutorial criado com sucesso!')
        return redirect('tutorial_detail', slug=tutorial.slug)
    return render(request, 'tutoriais/tutorial_create.html', {})


def tutorial_list(request):
    tutoriais = Tutoriais.objects.all().order_by('-data_criacao')
    return render(request, 'tutoriais/tutorial_list.html', {'tutoriais': tutoriais})


def tutorial_detail(request, slug):
    tutorial = get_object_or_404(Tutoriais, slug=slug)
    return render(request, 'tutoriais/tutorial_detail.html', {'tutorial': tutorial})


def tutoriais_lista(request):
    categoria = request.GET.get('categoria')
    if categoria:
        tutoriais = Tutoriais.objects.filter(categoria=categoria).order_by('-data_criacao')
    else:
        tutoriais = Tutoriais.objects.all().order_by('-data_criacao')
    categorias = Tutoriais.objects.values_list('categoria', flat=True).distinct()
    categorias = sorted(set([c.strip().title() for c in categorias if c]))
    return render(request, 'tutoriais/lista_tutoriais.html', {
        'tutoriais': tutoriais,
        'categorias': categorias,
        'categoria_ativa': categoria,
    })


def tutoriais_detalhe(request, slug):
    tutorial = get_object_or_404(Tutoriais, slug=slug)
    return render(request, 'tutoriais/tutoriais_detalhe.html', {'tutorial': tutorial})