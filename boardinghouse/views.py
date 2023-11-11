from django.shortcuts import render

# Create your views here.
def boardinghouse(request):
    return render(request, 'boardinghouse/boardinghouse.html')