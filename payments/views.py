from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from boardinghouse.models import Room
from homepage.models import Feedback, Notice
from payments.forms import BillsForm, PaymentsForm
from payments.models import Bills, Payments
from tenants.models import Tenant


# Create your views here.

@user_passes_test(lambda u: u.is_staff)
def utility_bill(request):
    rooms = Room.objects.filter(owner=request.user)
    bills = Bills.objects.filter(room__owner=request.user)

    form_room = Room.objects.filter(owner=request.user, is_archive=False)

    if request.method == "POST":
        if "button" in request.POST:
            if request.POST.get("button") == "add_utility":
                form = BillsForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.room = Room.objects.get(id=request.POST.get('room'))
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
                    room.price = request.POST.get('edit_rate')
                    room.save()
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
        'notice': Notice.objects.filter(is_viewed=False).count(),
        'form_room': form_room,

    })


@user_passes_test(lambda u: not u.is_superuser)
def payments(request):
    if request.user.is_superuser or request.user.is_staff:
        payments = Payments.objects.filter(room__owner=request.user)
    else:
        try:
            tenant = Tenant.objects.get(name__id=request.user.id)
            payments = Payments.objects.filter(tenant=tenant)
        except:
            tenant = None
            payments = None
    form_tenant = Tenant.objects.filter(owner=request.user, is_archive=False)
    form_room = Room.objects.filter(owner=request.user, is_archive=False)

    if request.method == "POST":
        if "button" in request.POST:
            if request.POST.get("button") == 'add_payment':

                form = PaymentsForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.room = Room.objects.get(id=request.POST.get('room'))
                    form.tenant = Tenant.objects.get(id=request.POST.get('tenant'))
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
        'form_tenant': form_tenant,
        'form_room': form_room,

    })

@user_passes_test(lambda u: not u.is_superuser)
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

@user_passes_test(lambda u: u.is_staff)
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

@user_passes_test(lambda u: u.is_staff)
def collectibles(request):
    #########################
    tenants = Tenant.objects.filter(owner=request.user)
    for tenant in tenants:
        if tenant.add_month < datetime.now().date():
            print("add month is less than now")
            print("late")
            tenant.previous_balance += tenant.current_balance
            tenant.current_balance = 0
            tenant.add_month = tenant.add_month + timedelta(days=30)

            tenant.save()
        else:
            print("add month is greater than now")
            print("not late")
            # get all payments
            payments = Payments.objects.filter(tenant=tenant)
            print(payments)
            total = 0
            print(total)
            for payment in payments:
                total += float(payment.amount)
            tenant.amount_paid = total
            tenant.save()


    #########################
    tenants = Tenant.objects.filter(room__isnull=False, owner=request.user)

    collectibles_lists = []

    for tenant in tenants:
        bills = Bills.objects.filter(room=tenant.room)
        total_bills = 0
        if bills:
            for bill in bills:
                total_bills += float(bill.rate)

        total_due = 0
        try:
            total_due = float(tenant.previous_balance) + float(total_bills)
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
            current_balance = float(total_due) - float(tenant.amount_paid)
            tenant.current_balance = current_balance
            tenant.save()
        except Exception as e:
            print("error")
            print(e)




        collectibles_lists.append({
            'tenant': tenant.name.get_full_name(),
            'room': tenant.room.name,
            'monthly_due': total_bills,
            'previous_balance': tenant.previous_balance,
            'total_due': total_due,
            'amount_paid': tenant.amount_paid,
            'current_balance': current_balance,
        })




    return render(request, 'payments/collectibles.html',{
        'tenants': tenants,
        'collectibles_lists': collectibles_lists,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),

    })