from .models import Tutoriais

def latest_tutorials(request):
    """Context processor to provide latest 3 tutorials and categories to all templates"""
    try:
        latest_tutorials = Tutoriais.objects.all().order_by('-data_criacao')[:3]
        categorias = Tutoriais.objects.values_list('categoria', flat=True).distinct()
        categorias = sorted(set([c.strip().title() for c in categorias if c]))
        return {
            'latest_tutorials': latest_tutorials,
            'categorias': categorias,
            'categoria_ativa': request.GET.get('categoria')
        }
    except:
        return {
            'latest_tutorials': [],
            'categorias': [],
            'categoria_ativa': None
        }