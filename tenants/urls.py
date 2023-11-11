from django.urls import path

from tenants import views

urlpatterns = [
    path('tenants_profile/', views.tenants_profile, name='tenants_profile'),
]