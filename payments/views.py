from django.shortcuts import render

# Create your views here.
def utility_bill(request):
    return render(request, 'payments/utility-bill.html')