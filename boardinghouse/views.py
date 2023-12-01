from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from tenants.models import Tenant
from .forms import BoardingHouseForms, RoomForm
from .models import BoardingHouse, Room


# Create your views here.

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def boardinghouse(request):
    boardinghouses = BoardingHouse.objects.filter(owner=request.user)

    if request.method == 'POST':
        forms = BoardingHouseForms(request.POST, request.FILES)
        print("button" in request.POST)

        if "button" in request.POST:
            print(request.POST.get('button'))
            if request.POST.get('button') == 'add_bhouse':
                try:
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
                except Exception as e:
                    messages.error(request, 'Error adding boarding house')
                    print('Error adding boarding house', e)
                    return redirect('boardinghouse')

            elif request.POST.get('button') == 'delete_bhouse':
                try:
                    id = request.POST.get('delete_id')
                    boardinghouse = get_object_or_404(BoardingHouse, id=id, owner=request.user)
                    boardinghouse.delete()
                    messages.success(request, 'Boarding House has been deleted successfully')
                    print('Boarding House has been deleted successfully')
                    return redirect('boardinghouse')
                except Exception as e:
                    messages.error(request, 'Error deleting boarding house')
                    print('Error deleting boarding house', e)
                    return redirect('boardinghouse')
    else:
        forms = BoardingHouseForms()

    return render(request, 'boardinghouse/boardinghouse.html', {
        'form': forms,
        'boardinghouses': boardinghouses,
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def boardinghouse_detail(request, id):
    boardinghouse = get_object_or_404(BoardingHouse, id=id, owner=request.user)
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

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def rooms(request):
    rooms = Room.objects.filter(owner=request.user)

    if request.method == "POST":
        forms = RoomForm(request.POST, request.FILES)
        if "button" in request.POST:
            if request.POST.get("button") == "add_room":
                if forms.is_valid():
                    room = forms.save(commit=False)
                    room.owner = request.user
                    room.save()
                    messages.success(request, 'Room has been added successfully')
                    print('Room has been added successfully')
                    return redirect('rooms')
                else:
                    messages.error(request, 'Error adding room')
                    print('Error adding room', forms.errors)
                    return redirect('rooms')
            elif request.POST.get("button") == "delete_room":
                try:
                    id = request.POST.get('delete_id')
                    room = get_object_or_404(Room, id=id, owner=request.user)
                    room.delete()
                    messages.success(request, 'Room has been deleted successfully')
                    print('Room has been deleted successfully')
                    return redirect('rooms')
                except Exception as e:
                    messages.error(request, 'Error deleting room')
                    print('Error room', e)
                    return redirect('rooms')

    else:
        forms = RoomForm()

    return render(request, 'boardinghouse/rooms.html', {
        'rooms': rooms,
        'form': forms,
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def rooms_detail(request, id):
    room = get_object_or_404(Room, id=id, owner=request.user)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room has been updated successfully')
            print('Room has been updated successfully')
            return redirect('rooms_detail', id=id)
        else:
            messages.error(request, 'Error updating room')
            print('Error updating room', form.errors)
            return redirect('rooms_detail', id=id)


    return render(request, 'boardinghouse/rooms_detail.html',{
        'room': room,
        'form': form,
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def manage_rooms(request):
    tenants = Tenant.objects.filter(owner=request.user, room__isnull=False)
    users = Tenant.objects.filter(owner=request.user, room__isnull=True)
    rooms = Room.objects.filter(boardinghouse__owner=request.user, owner=request.user)

    if request.method == "POST":
        if "button" in request.POST:
            if request.POST.get("button") == "add_assignment":
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
            elif request.POST.get("button") == "delete_assignment":
                try:
                    id = request.POST.get('id_delete')
                    print(id)
                    tenant = get_object_or_404(Tenant, id=id, owner=request.user)
                    tenant.room = None
                    tenant.save()
                    messages.success(request, 'Tenant has been deleted successfully')
                    print('Tenant has been deleted successfully')
                    return redirect('manage_rooms')
                except Exception as e:
                    messages.error(request, 'Error deleting tenant')
                    print('Error deleting tenant', e)
                    return redirect('manage_rooms')
            elif request.POST.get("button") == "edit_assignment":
                try:
                    name = request.POST.get("name")
                    room = request.POST.get("room")
                    room = get_object_or_404(Room, id=room, owner=request.user)
                    date = request.POST.get("date_start")

                    tenant = get_object_or_404(Tenant, name__username=name, owner=request.user)
                    tenant.room = room
                    tenant.date_start = date
                    tenant.save()
                    messages.success(request, 'Tenant has been edited successfully')
                    print('Tenant has been edited successfully')
                    return redirect('manage_rooms')



                except Exception as e:
                    messages.error(request, 'Error editing tenant')
                    print('Error editing tenant', e)
                    return redirect('manage_rooms')







    return render(request, 'boardinghouse/manage_rooms.html', {

        'tenants': tenants,
        'users': users,
        'rooms': rooms,
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def manage_rooms_detail(request, id):



    return render(request, 'boardinghouse/manage_rooms_detail.html')

def beds(request):
    return render(request, 'boardinghouse/beds.html')


def beds_assignment(request):
    return render(request, 'boardinghouse/beds_assignment.html')


