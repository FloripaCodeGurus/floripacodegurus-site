from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tutoriais


def tutoriais(request):
    try:
        tutoriais = Tutoriais.objects.all().order_by('-data_criacao')
        return render(request, 'tutoriais/tutoriais.html', {'tutoriais': tutoriais})
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'tutoriais/tutoriais.html', {'tutoriais': []})

@login_required
def tutorial_create(request):
    if request.method == 'POST':
        tutorial = Tutoriais(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            introducao=request.POST.get('introducao'),
            conceitos=request.POST.get('conceitos'),
            exemplos=request.POST.get('exemplos'),
            conclusao=request.POST.get('conclusao'),
            autor=f"{request.user.first_name} {request.user.last_name}",
            categoria=request.POST.get('categoria'),
            nivel=request.POST.get('nivel')
        )
        if request.FILES.get('imagem'):
            tutorial.imagem = request.FILES['imagem']
        tutorial.save()
        messages.success(request, 'Tutorial criado com sucesso!')
        return redirect('tutoriais_detalhe', slug=tutorial.slug)
    return render(request, 'tutoriais/tutorial_create.html', {})


# def tutorial_list(request):
#     tutoriais = Tutoriais.objects.all().order_by('-data_criacao')
#     return render(request, 'tutoriais/tutorial_list.html', {'tutoriais': tutoriais})


# def tutorial_detail(request, slug):
#     tutorial = get_object_or_404(Tutoriais, slug=slug)
    
#     related_tutorials = Tutoriais.objects.filter(
#         categoria=tutorial.categoria
#     ).exclude(slug=slug).order_by('-data_criacao')[:3]
    
#     if related_tutorials.count() < 3:
#         remaining_count = 3 - related_tutorials.count()
#         other_tutorials = Tutoriais.objects.exclude(
#             slug=slug
#         ).exclude(
#             slug__in=[t.slug for t in related_tutorials]
#         ).order_by('-data_criacao')[:remaining_count]
        
#         all_related = list(related_tutorials) + list(other_tutorials)
#     else:
#         all_related = related_tutorials
    
#     return render(request, 'tutoriais/tutorial_detail.html', {
#         'tutorial': tutorial,
#         'related_tutorials': all_related
    # })


def tutoriais_lista(request):
    try:
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
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'tutoriais/lista_tutoriais.html', {
            'tutoriais': [],
            'categorias': [],
            'categoria_ativa': categoria,
        })

def tutoriais_detalhe(request, slug):
    tutorial = get_object_or_404(Tutoriais, slug=slug)
    return render(request, 'tutoriais/tutoriais_detalhe.html', {'tutorial': tutorial})

@login_required
def tutorial_edit(request, slug):
    tutorial = get_object_or_404(Tutoriais, slug=slug, autor=f"{request.user.first_name} {request.user.last_name}")
    
    if request.method == 'POST':
        tutorial.titulo = request.POST.get('titulo')
        tutorial.descricao = request.POST.get('descricao')
        tutorial.introducao = request.POST.get('introducao')
        tutorial.conceitos = request.POST.get('conceitos')
        tutorial.exemplos = request.POST.get('exemplos')
        tutorial.conclusao = request.POST.get('conclusao')
        tutorial.categoria = request.POST.get('categoria')
        tutorial.nivel = request.POST.get('nivel')
        
        if request.FILES.get('imagem'):
            tutorial.imagem = request.FILES['imagem']
        
        tutorial.save()
        messages.success(request, 'Tutorial atualizado com sucesso!')
        return redirect('tutoriais_detalhe', slug=tutorial.slug)
    
    return render(request, 'tutoriais/tutorial_edit.html', {'tutorial': tutorial})

def tutorial_delete(request, slug):
    pass