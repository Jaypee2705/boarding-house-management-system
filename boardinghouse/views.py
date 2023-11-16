from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import BoardingHouseForms
from .models import BoardingHouse


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
    return render(request, 'boardinghouse/rooms.html')

def manage_rooms(request):
    return render(request, 'boardinghouse/manage_rooms.html')

def beds(request):
    return render(request, 'boardinghouse/beds.html')


def beds_assignment(request):
    return render(request, 'boardinghouse/beds_assignment.html')