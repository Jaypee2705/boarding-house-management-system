from django.urls import path

from tenants import views

urlpatterns = [
    path('tenants/', views.tenants_profile, name='tenants_profile'),
    path('tenants/archive/', views.tenant_archive, name='tenant_archive'),
]