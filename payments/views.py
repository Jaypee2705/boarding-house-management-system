import datetime

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from boardinghouse.models import Room
from homepage.models import Feedback, Notice
from payments.forms import BillsForm, PaymentsForm
from payments.models import Bills, Payments
from tenants.models import Tenant


# Create your views here.

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def utility_bill(request):
    rooms = Room.objects.filter(owner=request.user)
    bills = Bills.objects.filter(room__owner=request.user)

    if request.method == "POST":
        if "button" in request.POST:
            if request.POST.get("button") == "add_utility":
                form = BillsForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Utility bill added successfully')
                    return redirect('utility-bill')
                else:
                    messages.error(request, 'Error adding utility bill')
                    return redirect('utility-bill')
            elif request.POST.get("button") == "delete_utility":
                try:
                    bill = Bills.objects.get(id=request.POST.get('id_delete'))
                    bill.delete()
                    messages.success(request, 'Utility bill deleted successfully')
                    return redirect('utility-bill')
                except:
                    messages.error(request, 'Error deleting utility bill')
                    return redirect('utility-bill')
            elif request.POST.get("button") == "edit_utility":
                try:
                    room = Room.objects.get(id=request.POST.get('edit_room'))
                    bill = Bills.objects.get(id=request.POST.get('edit_id'))
                    bill.room = room
                    bill.bills = request.POST.get('edit_bills')
                    bill.rate = request.POST.get('edit_rate')
                    bill.save()
                    messages.success(request, 'Utility bill edited successfully')
                    return redirect('utility-bill')
                except:
                    messages.error(request, 'Error editing utility bill')
                    return redirect('utility-bill')
    else:
        form = BillsForm()

    return render(request, 'payments/utility-bill.html',{
        'rooms': rooms,
        'form': form,
        'bills': bills,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),

    })


@user_passes_test(lambda u: u.is_authenticated)
def payments(request):
    if request.user.is_superuser or request.user.is_staff:
        payments = Payments.objects.filter(room__owner=request.user)
    else:
        tenant = Tenant.objects.get(name__id=request.user.id)
        payments = Payments.objects.filter(tenant=tenant)
    if request.method == "POST":
        if "button" in request.POST:
            if request.POST.get("button") == 'add_payment':

                form = PaymentsForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Payment added successfully')
                    return redirect('payments')
                else:
                    messages.error(request, 'Error adding payment')
                    return redirect('payments')
            elif request.POST.get("button") == 'delete_payment':
                try:
                    payment = Payments.objects.get(id=request.POST.get('id_delete'))
                    payment.delete()
                    messages.success(request, 'Payment deleted successfully')
                    return redirect('payments')
                except:
                    messages.error(request, 'Error deleting payment')
                    return redirect('payments')
    else:
        form = PaymentsForm()


    return render(request, 'payments/payments.html',{
        'payments': payments,
        'form': form,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),

    })

@user_passes_test(lambda u: u.is_authenticated)
def payments_info(request, id):
    payment = Payments.objects.get(id=id)

    form = PaymentsForm(instance=payment)

    if request.method == "POST":
        form = PaymentsForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment edited successfully')
            return redirect('payments')
        else:
            messages.error(request, 'Error editing payment')
            return redirect('payments')



    return render(request, 'payments/payments-info.html',{
        'payment': payment,
        'form': form,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),

    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def income(request):


    """
    [
        {
            month: 'January',
            income: 10000,
        },
        {
            month: 'February',
            income: 10000,
        }

    ]
    """
    # create a list of dictionaries of names of the months and income
    # get all the months of payments
    payments = Payments.objects.filter(room__owner=request.user)
    months = []
    for payment in payments:
        total_amount = 0
        tempdict = {}
        if not any(payment.date.strftime('%B') in d['month'] for d in months):

            tempdict["month"] = payment.date.strftime('%B')
            months.append(tempdict)
        else:
            pass

    # get the total amount of payments per month
    for month in months:
        total_amount = 0
        for payment in payments:
            if month["month"] == payment.date.strftime('%B'):
                total_amount += float(payment.amount)
        month["income"] = total_amount







    return render(request, 'payments/income.html',{
        # 'income_list': income_list,
        'months': months,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),

    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def collectibles(request):
    tenants = Tenant.objects.filter(room__isnull=False, owner=request.user)

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
        'feedback': Feedback.objects.filter(is_viewed=False).count(),

    })