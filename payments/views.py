from django.shortcuts import render

# Create your views here.
def utility_bill(request):
    return render(request, 'payments/utility-bill.html')


def payments(request):
    return render(request, 'payments/payments.html')


def income(request):
    return render(request, 'payments/income.html')


def collectibles(request):
    return render(request, 'payments/collectibles.html')