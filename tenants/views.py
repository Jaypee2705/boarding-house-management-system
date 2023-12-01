from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Tenant

# Create your views here.


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def tenants_profile(request):
    # get all Users that is not a superuser and staff
    users = User.objects.filter(tenant__isnull=True).exclude(is_superuser=True).exclude(is_staff=True)
    tenants = Tenant.objects.filter(owner=request.user)
    if request.method == "POST":
        name = request.POST.get('user')
        user_instance = User.objects.get(id=name)
        # create tenant object
        tenant = Tenant(name=user_instance)
        tenant.owner = request.user
        tenant.save()
        messages.success(request, 'Tenant added successfully!')
        return redirect('tenants_profile')


    return render(request, 'tenants/tenants_profile.html',{
        'users': users,
        'tenants': tenants

    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_tenants(request):
    return render(request, 'tenants/add_tenants.html')