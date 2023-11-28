from django.contrib import messages
from django.shortcuts import render, redirect

from boardinghouse.models import Room
from payments.forms import BillsForm
from payments.models import Bills


# Create your views here.
def utility_bill(request):
    rooms = Room.objects.all()
    bills = Bills.objects.all()

    if request.method == "POST":
        form = BillsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utility bill added successfully')
            return redirect('utility-bill')
        else:
            messages.error(request, 'Error adding utility bill')
            return redirect('utility-bill')
    else:
        form = BillsForm()

    return render(request, 'payments/utility-bill.html',{
        'rooms': rooms,
        'form': form,
        'bills': bills,

    })


def payments(request):
    return render(request, 'payments/payments.html')


def income(request):
    return render(request, 'payments/income.html')


def collectibles(request):
    return render(request, 'payments/collectibles.html')