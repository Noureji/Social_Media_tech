from django.shortcuts import render ,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm 
from django.contrib.auth.models import User
from django.contrib.auth import login as is_login
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.
from django.contrib import messages
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)  # <-- important: request.FILES
        if form.is_valid():
            user = form.save()

            # si avatar fourni, on l'enregistre dans le profile
            avatar = form.cleaned_data.get('avatar')
            if avatar:
                user.profile.avatar = avatar
                user.profile.save()

            is_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']

        user.save()
        profile.save()

        return redirect('profile')

    return render(request, 'profil.html')
