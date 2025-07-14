from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

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

@login_required
def profile_create(request):
    return render(request, 'users/profile_create.html', {'user': request.user})

@login_required
def profile_list(request):
    users = CustomUser.objects.filter(is_active=True).order_by('first_name')
    return render(request, 'users/profile_list.html', {'users': users})

@login_required
def profile_detail(request):
    user_id = request.GET.get('id')
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user
    return render(request, 'users/profile_detail.html', {'profile_user': user})