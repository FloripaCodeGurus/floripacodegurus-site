from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.autor_github_account = request.POST.get('autor_github_account', user.autor_github_account)
        user.autor_linkedin_account = request.POST.get('autor_linkedin_account', user.autor_linkedin_account)
        
        if request.FILES.get('autor_picture'):
            user.autor_picture = request.FILES['autor_picture']
        
        user.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('profile')
    
    return render(request, 'users/profile.html', {'user': request.user})