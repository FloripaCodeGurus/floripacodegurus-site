from .models import Tutoriais

def latest_tutorials(request):
    """Context processor to provide latest 3 tutorials to all templates"""
    try:
        latest_tutorials = Tutoriais.objects.all().order_by('-data_criacao')[:3]
        return {'latest_tutorials': latest_tutorials}
    except:
        return {'latest_tutorials': []}