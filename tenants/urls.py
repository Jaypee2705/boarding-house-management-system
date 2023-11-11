from django.urls import path

from tenants import views

urlpatterns = [
    path('tenants_profile/', views.tenants_profile, name='tenants_profile'),
    path('tenants_profile/add/', views.add_tenants, name='add_tenants'),
]