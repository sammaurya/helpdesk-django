from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from .admin import  AddUserForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

# Create your views here.

def support(request):
    pass

def signup_view(request):
    if request.method == 'POST':
        form = AddUserForm(data=request.POST)
        if form.is_valid():
            user =  form.save()
            return redirect('login')
    else:
        form = AddUserForm()
        args = {'form' : form}
        return render(request, 'user/signup.html', args)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('list_tickets'))
        else:
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'registration/login.html', {})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
