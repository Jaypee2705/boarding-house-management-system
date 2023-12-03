from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from homepage.models import Feedback
from .models import Tenant

# Create your views here.


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def tenants_profile(request):
    users = User.objects.filter(tenant__isnull=True).exclude(is_superuser=True).exclude(is_staff=True)
    if request.user.is_superuser:
        tenants = Tenant.objects.filter(is_archive=False)
    else:
        tenants = Tenant.objects.filter(owner=request.user, is_archive=False)
    if request.method == "POST":
        if request.POST.get("button") == "add":
            try:
                name = request.POST.get('user')
                user_instance = User.objects.get(id=name)
                # create tenant object
                tenant = Tenant(name=user_instance)
                tenant.owner = request.user
                tenant.address = request.POST.get('address')
                tenant.contact_number = request.POST.get('number')
                tenant.save()
                messages.success(request, 'Tenant added successfully!')
                return redirect('tenants_profile')
            except Exception as e:
                print(e)
                messages.error(request, e)
                return redirect('tenants_profile')
        elif request.POST.get("button") == "archive":
            try:
                tenant = Tenant.objects.get(id=request.POST.get('delete_id'))
                tenant.is_archive = True
                tenant.save()
                messages.success(request, 'Tenant archived successfully!')
                return redirect('tenants_profile')
            except Exception as e:
                print(e)
                messages.error(request, e)
                return redirect('tenants_profile')





    return render(request, 'tenants/tenants_profile.html',{
        'users': users,
        'tenants': tenants,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),

    })

@user_passes_test(lambda u: u.is_superuser)
def tenant_archive(request):
    tenants = Tenant.objects.filter(is_archive=True)

    if request.method == "POST":
        if request.POST.get("button") == "restore":
            try:
                tenant = Tenant.objects.get(id=request.POST.get('restore_id'))
                tenant.is_archive = False
                tenant.save()
                messages.success(request, 'Tenant restored successfully!')
                return redirect('tenants_profile')
            except Exception as e:
                print(e)
                messages.error(request, e)
                return redirect('tenants_profile')
        elif request.POST.get("button") == "delete":
            try:
                tenant = Tenant.objects.get(id=request.POST.get('delete_id'))
                tenant.delete()
                messages.success(request, 'Tenant deleted successfully!')
                return redirect('tenants_profile')
            except Exception as e:
                print(e)
                messages.error(request, e)
                return redirect('tenants_profile')

    return render(request, 'tenants/tenant_archive.html',{
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'tenants': tenants,
    })
