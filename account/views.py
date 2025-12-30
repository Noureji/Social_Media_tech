from django.shortcuts import render ,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm 
from django.contrib.auth.models import User
from django.contrib.auth import login as is_login
# Create your views here.
def signup(request):
    if request.method == "POST":
        form =SignUpForm(request.POST)
        if form.is_valid():
                user=form.save()
                is_login(request,user)
                return redirect('index')
    else :
        form = SignUpForm()
    return render(request,'signup.html' ,{'form':form})