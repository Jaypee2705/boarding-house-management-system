from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from tenants.models import Tenant
from .forms import BoardingHouseForms, RoomForm
from .models import BoardingHouse, Room


# Create your views here.


def boardinghouse(request):
    boardinghouses = BoardingHouse.objects.all()

    if request.method == 'POST':
        forms = BoardingHouseForms(request.POST, request.FILES)
        if forms.is_valid():
            boardinghouse = forms.save(commit=False)
            boardinghouse.owner = request.user
            boardinghouse.save()
            messages.success(request, 'Boarding House has been added successfully')
            print('Boarding House has been added successfully')
            return redirect('boardinghouse')
        else:
            messages.error(request, 'Error adding boarding house')
            print('Error adding boarding house', forms.errors)
            return redirect('boardinghouse')
    else:
        forms = BoardingHouseForms()

    return render(request, 'boardinghouse/boardinghouse.html', {
        'form': forms,
        'boardinghouses': boardinghouses,
    })


def boardinghouse_detail(request, id):
    boardinghouse = BoardingHouse.objects.get(id=id)
    form = BoardingHouseForms(instance=boardinghouse)
    if request.method == "POST":
        form = BoardingHouseForms(request.POST, request.FILES, instance=boardinghouse)
        if form.is_valid():
            form.save()
            messages.success(request, 'Boarding House has been updated successfully')
            print('Boarding House has been updated successfully')
            return redirect('boardinghouse_detail', id=id)
        else:
            messages.error(request, 'Error updating boarding house')
            print('Error updating boarding house', form.errors)
            return redirect('boardinghouse_detail', id=id)

    return render(request, 'boardinghouse/boardinghouse_detail.html', {
        'boardinghouse': boardinghouse,
        'form': form,
    })


def rooms(request):
    rooms = Room.objects.all()

    if request.method == "POST":
        forms = RoomForm(request.POST, request.FILES)
        if forms.is_valid():
            room = forms.save(commit=False)
            room.save()
            messages.success(request, 'Room has been added successfully')
            print('Room has been added successfully')
            return redirect('rooms')
        else:
            messages.error(request, 'Error adding room')
            print('Error adding room', forms.errors)
            return redirect('rooms')
    else:
        forms = RoomForm()

    return render(request, 'boardinghouse/rooms.html', {
        'rooms': rooms,
        'form': forms,
    })


def manage_rooms(request):
    tenants = Tenant.objects.filter(owner=request.user, room__isnull=False)
    users = Tenant.objects.filter(owner=request.user, room__isnull=True)
    rooms = Room.objects.filter(boardinghouse__owner=request.user)

    if request.method == "POST":
        name = request.POST.get('name')
        room = request.POST.get('room')
        date = request.POST.get('date_start')
        try:
            tenant = Tenant.objects.get(id=name)
            room = Room.objects.get(id=room)
            tenant.room = room
            tenant.date_start = date
            tenant.save()
            messages.success(request, 'Tenant has been added successfully')
            print('Tenant has been added successfully')
            return redirect('manage_rooms')
        except Exception as e:
            messages.error(request, 'Error adding tenant')
            print('Error adding tenant', e)
            return redirect('manage_rooms')

    return render(request, 'boardinghouse/manage_rooms.html', {

        'tenants': tenants,
        'users': users,
        'rooms': rooms,
    })


def beds(request):
    return render(request, 'boardinghouse/beds.html')


def beds_assignment(request):
    return render(request, 'boardinghouse/beds_assignment.html')
