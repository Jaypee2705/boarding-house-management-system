from django.contrib import messages
from django.shortcuts import render, redirect
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

    return render(request, 'boardinghouse/boardinghouse.html',{
        'form': forms,
        'boardinghouses': boardinghouses,
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


    return render(request, 'boardinghouse/rooms.html',{
        'rooms': rooms,
        'form': forms,
    })

def manage_rooms(request):
    return render(request, 'boardinghouse/manage_rooms.html')

def beds(request):
    return render(request, 'boardinghouse/beds.html')


def beds_assignment(request):
    return render(request, 'boardinghouse/beds_assignment.html')