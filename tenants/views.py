from django.shortcuts import render

# Create your views here.
def tenants_profile(request):
    return render(request, 'tenants/tenants_profile.html')
