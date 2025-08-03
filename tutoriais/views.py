from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tutoriais


def tutoriais(request):
    try:
        categoria = request.GET.get('categoria')
        if categoria:
            tutoriais = Tutoriais.objects.filter(categoria=categoria).order_by('-data_criacao')
        else:
            tutoriais = Tutoriais.objects.all().order_by('-data_criacao')
        categorias = Tutoriais.objects.values_list('categoria', flat=True).distinct()
        categorias = sorted(set([c.strip().title() for c in categorias if c]))
        return render(request, 'tutoriais/tutoriais.html', {
            'tutoriais': tutoriais,
            'categorias': categorias,
            'categoria_ativa': categoria,
        })
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'tutoriais/tutoriais.html', {
            'tutoriais': [],
            'categorias': [],
            'categoria_ativa': categoria,
        })

@login_required
def tutorial_create(request):
    if request.method == 'POST':
        tutorial = Tutoriais(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            introducao=request.POST.get('introducao'),
            conceitos=request.POST.get('conceitos'),

            exemplo1=request.POST.get('exemplo1'),
            exemplo2=request.POST.get('exemplo2'),
            exemplo3=request.POST.get('exemplo3'),
            conclusao=request.POST.get('conclusao'),
            autor=request.user,
            categoria=request.POST.get('categoria'),
            nivel=request.POST.get('nivel')
        )
        if request.FILES.get('imagem'):
            tutorial.imagem = request.FILES['imagem']
        tutorial.save()
        messages.success(request, 'Tutorial criado com sucesso!')
        return redirect('tutorial_detail', slug=tutorial.slug)
    return render(request, 'tutoriais/tutorial_create.html', {})


def tutoriais_detalhe(request, slug):
    try:
        tutorial = get_object_or_404(Tutoriais, slug=slug)
        # return render(request, 'tutoriais/tutoriais_detalhe.html', {'tutorial': tutorial})
        return render(request, 'tutoriais/tutorial_detail.html', {'tutorial': tutorial})
    except Tutoriais.DoesNotExist:
        messages.error(request, 'Tutorial não encontrado.')
        return redirect('tutoriais')

@login_required
def tutorial_edit(request, slug):
    tutorial = get_object_or_404(Tutoriais, slug=slug, autor=request.user)
    
    if request.method == 'POST':
        tutorial.titulo = request.POST.get('titulo')
        tutorial.descricao = request.POST.get('descricao')
        tutorial.introducao = request.POST.get('introducao')
        tutorial.conceitos = request.POST.get('conceitos')
        tutorial.exemplo1 = request.POST.get('exemplo1')
        tutorial.exemplo2 = request.POST.get('exemplo2')
        tutorial.exemplo3 = request.POST.get('exemplo3')
        tutorial.conclusao = request.POST.get('conclusao')
        tutorial.categoria = request.POST.get('categoria')
        tutorial.nivel = request.POST.get('nivel')
        
        if request.FILES.get('imagem'):
            tutorial.imagem = request.FILES['imagem']
        
        tutorial.save()
        messages.success(request, 'Tutorial atualizado com sucesso!')
        return redirect('tutorial_detail', slug=tutorial.slug)
    
    return render(request, 'tutoriais/tutorial_edit.html', {'tutorial': tutorial})

@login_required
def tutorial_delete(request, slug):
    tutorial = get_object_or_404(Tutoriais, slug=slug, autor=request.user)
    
    if request.method == 'POST':
        tutorial.delete()
        messages.success(request, 'Tutorial deletado com sucesso!')
        return redirect('tutoriais')
    
    return render(request, 'tutoriais/tutorial_delete.html', {'tutorial': tutorial})