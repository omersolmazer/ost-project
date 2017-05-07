
from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Resource, Reservations

def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

