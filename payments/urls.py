from django.urls import path

from payments import views

urlpatterns = [
    path('utility-bill/', views.utility_bill, name='utility-bill'),
    path('payments/', views.payments, name='payments'),
    path('payments/<int:id>/', views.payments_info, name='payments-info'),
    path('payments/transient/', views.transient, name='transient'),
    path('payments/transient/<int:id>/', views.transient_info, name='transient-info'),
    path('income/', views.income, name='income'),
    path('collectibles/', views.collectibles, name='collectibles'),
    ]
