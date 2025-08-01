from django.shortcuts import render
from .models import Newsletter

# Create your views here.

def inscrever(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            # Checar se o email já existe
            if Newsletter.objects.filter(email=email).exists():
                return render(request, "newsletter/erro.html", {"message": "Este email já está inscrito."})
            newsletter = Newsletter(email=email)
            newsletter.save()
            return render(request, "newsletter/sucesso.html", {"email": email})
    return render(request, "newsletter/inscricao.html")


    
