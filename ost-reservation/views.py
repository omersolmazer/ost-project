from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Resource, Reservations
from .forms import SignUpForm, ResourceCreateForm
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


def resources(request):
    if request.method == 'POST':
        form = ResourceCreateForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            print(start_time)
            print(end_time)
            tags = form.cleaned_data.get('tag')
            if not tags:
                tags = ''
            resource = Resource(owner=request.user, name=name, start_time=start_time, end_time=end_time, tags=tags)
            resource.save()
            return render(request, 'resources.html', {'form':ResourceCreateForm(), 'resources': Resource.objects.all()})
        else:
            return render(request, 'resources.html', {'invalid':True, 'form':form, 'resources': Resource.objects.all()})
    else:
        resources = Resource.objects.all()
        return render(request, 'resources.html', { 'resources': resources, 'form':ResourceCreateForm() } )


def resource(request, resource_id=0):
    res = get_object_or_404(Resource, pk=resource_id)
    return render(request, 'resource.html', { 'resource': res } )


def err(request):
    return render(request, '404.html', {} )

def reservation(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation.html', { 'reservations': reservations } )

def clear_users():
    x = User.objects.all()
    x.delete()


def user_logout(request):
    logout(request)
    return render(request, 'index.html',{})
    
