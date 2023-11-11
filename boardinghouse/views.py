from django.shortcuts import render

# Create your views here.
def boardinghouse(request):
    return render(request, 'boardinghouse/boardinghouse.html')


def rooms(request):
    return render(request, 'boardinghouse/rooms.html')


def beds(request):
    return render(request, 'boardinghouse/beds.html')


def beds_assignment(request):
    return render(request, 'boardinghouse/beds_assignment.html')