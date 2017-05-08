from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Resource, Reservations
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


def index(request):
    if request.user and request.user.is_authenticated() :
        return render(request, 'index.html', {'user' : request.user})
    else:
        return render(request, 'index.html', {})

def users(request):
    users = User.objects.all()
    # clear_users()
    return render(request, 'users.html', {'users': users})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            user = User.objects.create_user(username=username, email=email, password=raw_password)
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print('Who? ' + username + '  ' + raw_password + '  ' + email)
            return redirect('/') 
    else:
        if request.user.is_authenticated():
            return redirect('/logout')
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'created':True})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if request.user.is_authenticated():
                return render(request, 'index.html', {'user':request.user})
            else:
                return render(request, 'login.html', {'invalid':True, 'form': AuthenticationForm()})
        else:
            return render(request, 'login.html', {'not_valid':True, 'form': AuthenticationForm()})

    else:
        if request.user.is_authenticated():
            return redirect('/logout')
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})


def clear_users():
    x = User.objects.all()
    x.delete()


def user_logout(request):
    logout(request)
    return render(request, 'login.html',{})
    
