from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
@login_required(login_url='login')
def homepage(request):
    if request.user.is_superuser:
        return redirect('dashboard')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')