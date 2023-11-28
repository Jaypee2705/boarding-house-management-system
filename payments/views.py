from django.contrib import messages
from django.shortcuts import render, redirect

from boardinghouse.models import Room
from payments.forms import BillsForm, PaymentsForm
from payments.models import Bills, Payments
from tenants.models import Tenant


# Create your views here.
def utility_bill(request):
    rooms = Room.objects.filter(owner=request.user)
    bills = Bills.objects.filter(room__owner=request.user)

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
    payments = Payments.objects.filter(room__owner=request.user)

    if request.method == "POST":
        form = PaymentsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment added successfully')
            return redirect('payments')
        else:
            messages.error(request, 'Error adding payment')
            return redirect('payments')
    else:
        form = PaymentsForm()


    return render(request, 'payments/payments.html',{
        'payments': payments,
        'form': form,

    })


def income(request):
    return render(request, 'payments/income.html')


def collectibles(request):
    tenants = Tenant.objects.filter(room__isnull=False)

    """
    [
        {
            tenant: 'John Doe',
            room: 'Room 1',
            monthly_due: 1000,
            previous_balance: 1000,
            total_due: 2000,
            amount_paid: 1000,
            current_balance: 1000,
        },
        {
            tenent: 'Jane Doe',
            room: 'Room 2',
            monthly_due: 1000,
            previous_balance: 1000,
            total_due: 2000,
            amount_paid: 1000,
            current_balance: 1000,
        }
    
    
    ]
    
    """
    collectibles_lists = []

    for tenant in tenants:

        total_due = 0
        try:
            total_due = float(tenant.previous_balance) + float(Bills.objects.get(room=tenant.room).rate)
        except:
            pass

        amount_paid = 0
        try:
            for payment in Payments.objects.filter(tenant=tenant):
                amount_paid += float(payment.amount)
        except:
            pass

        current_balance = 0
        try:
            current_balance = total_due - amount_paid
        except:
            pass
        collectibles_lists.append({
            'tenant': tenant.name.get_full_name(),
            'room': tenant.room.name,
            'monthly_due': Bills.objects.get(room=tenant.room).rate,
            'previous_balance': tenant.previous_balance,
            'total_due': total_due,
            'amount_paid': amount_paid,
            'current_balance': current_balance,
        })




    return render(request, 'payments/collectibles.html',{
        'tenants': tenants,
        'collectibles_lists': collectibles_lists,
    })