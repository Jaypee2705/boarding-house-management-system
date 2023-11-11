from django.urls import path

from payments import views

urlpatterns = [
    path('utility-bill/', views.utility_bill, name='utility-bill'),
    path('payments/', views.payments, name='payments'),
    ]
