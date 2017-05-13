from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Resource, Reservation
from .forms import SignUpForm, ResourceCreateForm, ReservationForm, SearchForm

from datetime import datetime
import pytz


def index(request):
    if request.user and request.user.is_authenticated() :
        all_resources = Resource.objects.all().order_by('-last_res_made')
        user_resources = request.user.resource_set.all().order_by('-last_res_made')
        user_reservations = Reservation.objects.filter(owner=request.user).order_by('-date', '-start_time')
        remove_old_reservations(user_reservations)
        return render(request, 'index.html', {'user' : request.user, 'user_resources': user_resources, 'all_resources': all_resources, 'user_reservations': user_reservations})

    else:
        return render(request, 'index.html', {})


def users(request):
    users = User.objects.all()
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
                return redirect('/index')
        return render(request, 'login.html', {'invalid':True, 'form': form})

    else:
        if request.user.is_authenticated():
            return redirect('/index')
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})


def reservations(request):
    return render(request, 'reservations.html', {})


def resources(request):
    if request.method == 'POST':
        form = ResourceCreateForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            tags = form.cleaned_data.get('tags')
            capacity = form.cleaned_data.get('capacity')
            last_res_made = datetime.now()
            if not tags:
                tags = ''
            resource = Resource(owner=request.user, name=name, start_time=start_time, end_time=end_time, tags=tags, last_res_made=last_res_made, capacity=capacity)
            resource.save()
            return render(request, 'resources.html', {'form':ResourceCreateForm(), 'resources': Resource.objects.all()})
        else:
            return render(request, 'resources.html', {'invalid':True, 'form':form, 'resources': Resource.objects.all()})
    else:
        resources = Resource.objects.all()
        return render(request, 'resources.html', { 'resources': resources, 'form':ResourceCreateForm() } )


def edit_resource(request, resource_id=0):
    if request.method == 'POST':
        form = ResourceCreateForm(request.POST)
        if form.is_valid():
            res = get_object_or_404(Resource, pk=resource_id)
            res.name = form.cleaned_data.get('name')
            res.start_time = form.cleaned_data.get('start_time')
            res.end_time = form.cleaned_data.get('end_time')
            tags = form.cleaned_data.get('tags')
            if not tags:
                tags = ''
            res.tags = tags
            res.save()
            return render(request, 'resource.html', {'resource':res, 'user':request.user})
        else:
            return render(request, 'edit.html', {'resource':get_object_or_404(Resource, pk=resource_id), 'user':request.user, 'form':form})

    else:
        if request.user:
            res = get_object_or_404(Resource, pk=resource_id)
            print(resource_id)
            if res.owner != request.user:
                return redirect('/index')
            else:
                form = ResourceCreateForm(instance=res)
                return render(request, 'edit.html', {'resource':res, 'user': request.user, 'form':form})
        else:
            return redirect('/index')


def cancel_reservation(request, reservation_id=0):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.user and reservation.owner == request.user:
        reservation.delete()
    return redirect('/index')


def resource(request, resource_id=0):
    if request.method == 'POST':
        form = ReservationForm(data=request.POST)
        if form.is_valid():
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            date = form.cleaned_data.get('date')
            res = get_object_or_404(Resource, pk=resource_id)

            if start_time < res.start_time:
                form.add_error('start_time', 'Cannot reserve before ' + str(res.start_time) + ' !')
                return render(request, 'resource.html', {'resource': res, 'form':form})

            elif end_time > res.end_time:
                form.add_error('end_time', 'Cannot reserve after ' + str(res.end_time) + ' !')
                return render(request, 'resource.html', {'resource': res, 'form':form})
            
            elif date < datetime.today().date():
                form.add_error('date', 'Cannot make reservations for past!')
                return render(request, 'resource.html', {'resource': res, 'form':form})

            count = 0
            for temp_res in res.reservation_set.all():
                if temp_res.date == date:
                    if start_time <= temp_res.start_time and end_time >= temp_res.start_time:
                        count += 1
                    elif start_time >= temp_res.start_time and start_time <= temp_res.end_time:
                        count += 1

            if count >= res.capacity:
                form.add_error('date', 'Resource is all booked for this time slot!')
                return render(request, 'resource.html', {'resource': res, 'form':form})

            for temp_reservation in request.user.reservation_set.all():
                if temp_reservation.date == date:
                    if start_time <= temp_reservation.start_time and end_time >= temp_reservation.start_time:
                        form.add_error('start_time', 'Cannot make reservation due to overlap!')
                        return render(request, 'resource.html', {'resource': res, 'form':form})
                    elif start_time >= temp_reservation.start_time and start_time <= temp_reservation.end_time:
                        form.add_error('start_time', 'Cannot make reservation due to overlap!')
                        return render(request, 'resource.html', {'resource': res, 'form':form})

            reservation = Reservation(start_time=start_time, end_time=end_time, date=date, owner=request.user, resource=res)
            reservation.save()
            body = 'You have made a reservation on ' + res.name +' on date ' + str(date) + ' starting from:' + str(start_time) + ' ending at: ' + str(end_time)
            
            new_date = datetime.combine(date, end_time)
            new_date = pytz.utc.localize(new_date)
            if new_date > res.last_res_made:
                res.last_res_made = new_date
            res.reserve_count += 1
            res.save()

            return render(request, 'resource.html', {'resource': res, 'form':ReservationForm()})
        else:
            res = get_object_or_404(Resource, pk=resource_id)
            return render(request, 'resource.html', {'resource': res, 'form':form})
    else:
        res = get_object_or_404(Resource, pk=resource_id)
        if request.user and res.owner == request.user:
            editable = True
        else:
            editable = False
        return render(request, 'resource.html', { 'resource': res, 'form':ReservationForm(), 'editable':editable } )


def user(request):
    if request.user:
        return render(request, 'user.html', { 'user':request.user })
    else:
        return redirect('/index.html')


def remove_old_reservations(reservations):
    for reservation in reservations:
            res_date_time = datetime.combine(reservation.date, reservation.end_time)
            res_date_time = pytz.utc.localize(res_date_time)
            if res_date_time < timezone.now():
                reservation.delete()


def search(request):
    if request.method =='GET':
        return render(request, 'searchResults.html', {'form': SearchForm(), 'is_get': True} )
    else:
        form = SearchForm(data=request.POST)
        resources = []
        if form.is_valid():
            term = form.cleaned_data.get('term')
            term = term.lower()
            for resource in Resource.objects.all():
                if term in resource.name.lower():
                    resources.append(resource)
                else:
                    for t in resource.tags.split(','):
                        if term in t.lower() and resource not in resources:
                            resources.append(resource)   
        return render(request, 'searchResults.html', {'form': SearchForm(),'resources': resources,'term': term})


def rss(request, resource_id=0):
    res = get_object_or_404(Resource, pk=resource_id)
    rss = res.reservation_set.all()
    rss = serializers.serialize("xml", rss, fields=('start_time', 'end_time', 'date'))
    return render(request, 'rss.html', {'rss':rss})


def reservation(request):
    reservations = Reservation.objects.all()
    remove_old_reservations(reservation)
    return render(request, 'reservation.html', { 'reservations': reservations } )


def reset(request):
    Resource.objects.all().delete()
    Reservation.objects.all().delete()
    
    return render(request, 'index.html', {})


def clear_users():
    x = User.objects.all()
    x.delete()


def user_logout(request):
    logout(request)
    return render(request, 'index.html',{})
    
