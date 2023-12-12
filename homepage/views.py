from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from boardinghouse.models import BoardingHouse, Room
from homepage.forms import FeedbackForms, NoticeForms, UserForm
from homepage.models import Feedback, Notice
from payments.models import Payments, TransientPayment
from tenants.models import Tenant


# Create your views here.
@login_required(login_url='login')
def homepage(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    elif request.user.is_staff:
        return redirect('dashboard_owner')
    elif request.user.is_active:
        return redirect('dashboard_tenant')

@user_passes_test(lambda u: u.is_authenticated )
def dashboard(request):
    if request.user.is_superuser:
        tenants = Tenant.objects.all()
        tenants_count = tenants.count()
        boardinghouses = BoardingHouse.objects.all()
        boardinghouses_count = boardinghouses.count()
        rooms = Room.objects.all()
        rooms_count = rooms.count()
        owner = User.objects.filter(is_superuser=False, is_staff=True).count()
    else:
        return redirect('homepage')


    return render(request, 'dashboard/dashboard.html',{
        'tenants_count': tenants_count,
        'boardinghouses_count': boardinghouses_count,
        'rooms_count': rooms_count,
        'owner': owner,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),

    })

@user_passes_test(lambda u: u.is_authenticated)
def dashboard_owner(request):
    # get all Payments in Payment
    if request.user.is_staff:
        income = 0
        payments = Payments.objects.filter(room__boardinghouse__owner=request.user)
        for payment in payments:
            income = float(income) + float(payment.amount)
        # get all tenants in Tenant
        tenants = Tenant.objects.filter(room__boardinghouse__owner=request.user).count()
        # get all rooms in Room
        rooms = Room.objects.filter(boardinghouse__owner=request.user).count()
        # get all boardinghouses in BoardingHouse
        boardinghouses = BoardingHouse.objects.filter(owner=request.user).count()


        """
            [
                {
                    "month: "January",
                    "income": 10000
                },
                {
                    "month: "February",
                    "income": 10000
                },
                {
                    "month: "March",
                    "income": 10000
                },
                {
                    "month: "April",
                    "income": 10000
                },
                {
                    "month: "May",
                    "income": 10000
                },
                {
                    "month: "June",
                    "income": 10000
                },
                {
                    "month: "July",
                    "income": 10000
                },
                {
                    "month: "August",
                    "income": 10000
                },
                {
                    "month: "September",
                    "income": 10000
                },
                {
                    "month: "October",
                    "income": 10000
                },
                {
                    "month: "November",
                    "income": 10000
                },
                {
                    "month: "December",
                    "income": 10000
                },
            ]
        """
        # get all payments in Payments
        payments = Payments.objects.filter(room__boardinghouse__owner=request.user)
        transient_payments = TransientPayment.objects.filter(room__boardinghouse__owner=request.user)

        monthly_income = []
        for i in range(1,13):
            monthly_income.append({
                "month": datetime(2021, i, 1).strftime("%B"),
                "income": 0,
            })
        for payment in payments:
            monthly_income[payment.date.month-1]["income"] += float(payment.amount)
        for transient_payment in transient_payments:
            monthly_income[transient_payment.date.month-1]["income"] += float(transient_payment.amount)


        print(monthly_income)


    else:
        return redirect('homepage')


    return render(request, 'dashboard/dashboard.html',{
        'income': income,
        'tenants': tenants,
        'rooms': rooms,
        'boardinghouses': boardinghouses,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),
        'monthly_income': monthly_income,

    })

@user_passes_test(lambda u: u.is_authenticated)
def dashboard_tenant(request):
    if not request.user.is_superuser and not request.user.is_staff:
        try:
            tenant = Tenant.objects.get(name__id=request.user.id)
            room = Room.objects.get(tenant=tenant)
        except Exception as e:
            tenant = None
            room = None
    else:
        return redirect('homepage')
    return render(request, 'dashboard/dashboard.html',{
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),
        'tenant': tenant,
        'room': room,

    })

@user_passes_test(lambda u: u.is_authenticated)
def notice(request):
    if request.user.is_superuser:
        notices = Notice.objects.filter(is_archived=False)
    elif request.user.is_staff:
        notices = Notice.objects.filter(boardinghouse__owner=request.user, is_archived=False)

    else:
        user = User.objects.get(id=request.user.id)
        try:
            tenant_instance = Tenant.objects.get(name__id=user.id)
            notices = Notice.objects.filter(boardinghouse = tenant_instance.room.boardinghouse, is_archived=False)
            for noti in notices:
                noti.is_viewed = True
                noti.save()
        except Exception as e:
            notices = None
    bhouses = BoardingHouse.objects.filter(owner=request.user, is_archive=False)

    if request.method == "POST":
        form = NoticeForms(request.POST)
        if "button" in request.POST:
            if request.POST.get("button") == "add_notice":

                if form.is_valid():
                    notice = form.save(commit=False)
                    notice.boardinghouse = BoardingHouse.objects.get(id=request.POST.get("boardinghouse"))
                    notice.save()
                    messages.success(request, 'Notice Submitted Successfully')
                    return redirect('notice')
                else:
                    messages.error(request, 'Notice Submission Failed')
                    return redirect('notice')
            elif request.POST.get("button") == "delete_notice":
                try:
                    notice = Notice.objects.get(id=request.POST.get("delete_id"))
                    notice.is_archived = True
                    notice.is_viewed = True
                    notice.save()
                    messages.success(request, 'Notice Archived Successfully')
                    return redirect('notice')
                except Exception as e:
                    messages.error(request, 'Notice Archived Failed')
                    print(e)
                    return redirect('notice')
    else:
        form = NoticeForms()

    return render(request, 'dashboard/notice.html',{
        'notices': notices,
        'form': form,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),
        'bhouses': bhouses,

    })

@user_passes_test(lambda u: u.is_superuser)
def notice_archive(request):
    notices = Notice.objects.filter(boardinghouse__owner=request.user, is_archived=True)


    if request.method == "POST":
        if request.POST.get("button") == "recover":
            try:
                notice = Notice.objects.get(id=request.POST.get("recover_id"))
                notice.is_archived = False
                notice.is_viewed = False
                notice.save()
                messages.success(request, 'Notice Recovered Successfully')
                return redirect('notice_archive')
            except Exception as e:
                messages.error(request, 'Notice Recovery Failed')
                print(e)
                return redirect('notice_archive')
        elif request.POST.get("button") == "delete":
            try:
                notice = Notice.objects.get(id=request.POST.get("delete_id"))
                notice.delete()
                messages.success(request, 'Notice Deleted Successfully')
                return redirect('notice_archive')
            except Exception as e:
                messages.error(request, 'Notice Deletion Failed')
                print(e)
                return redirect('notice_archive')



    return render(request, 'dashboard/notice_archive.html',{
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),
        'notices': notices,

    })


@user_passes_test(lambda u: u.is_authenticated)
def notice_detail(request, id):
    notice = Notice.objects.get(id=id)

    form = NoticeForms(instance=notice)

    if request.method == "POST":
        form = NoticeForms(request.POST, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.save()
            messages.success(request, 'Notice Updated Successfully')
            return redirect('notice')
        else:
            messages.error(request, 'Notice Update Failed')
            return redirect('notice')

    return render(request, 'dashboard/notice_detail.html',{
        'notice': notice,
        'form': form,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),

    })

@user_passes_test(lambda u: u.is_authenticated)
def feedbacks(request):
    if request.user.is_superuser:
        feedbacks = Feedback.objects.filter(is_archived=False)
        for feeds in feedbacks:
            feeds.is_viewed = True
            feeds.save()
    else:
        feedbacks = Feedback.objects.filter(user=request.user, is_archived=False)

    if request.method == "POST":
        if "button" in request.POST:
            if request.POST.get("button") == "add":


                form = FeedbackForms(request.POST)
                if form.is_valid():
                    feedback = form.save(commit=False)
                    feedback.user = request.user
                    feedback.save()
                    messages.success(request, 'Feedback Submitted Successfully')
                    return redirect('feedbacks')
                else:
                    messages.error(request, 'Feedback Submission Failed')
                    return redirect('feedbacks')
            elif request.POST.get("button") == "delete":
                try:
                    feedback = Feedback.objects.get(id=request.POST.get("delete_id"))
                    feedback.is_archived = True
                    feedback.is_viewed = True
                    feedback.save()
                    messages.success(request, 'Feedback Archived Successfully')
                    return redirect('feedbacks')
                except Exception as e:
                    messages.error(request, 'Feedback Archived Failed')
                    print(e)
                    return redirect('feedbacks')
            elif request.POST.get("button") == "edit":
                try:
                    feedback = Feedback.objects.get(id=request.POST.get("edit_id"))
                    feedback.feedback = request.POST.get("edit_feedback")
                    feedback.date = datetime.now()
                    feedback.save()
                    messages.success(request, 'Feedback Updated Successfully')
                    return redirect('feedbacks')
                except Exception as e:
                    messages.error(request, 'Feedback Update Failed')
                    print(e)
                    return redirect('feedbacks')

    else:
        form = FeedbackForms()

    return render(request, 'dashboard/feedbacks.html',{
        'feedbacks': feedbacks,
        'form': form,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),

    })

@user_passes_test(lambda u: u.is_superuser)
def feedbacks_archive(request):
    feedbacks = Feedback.objects.filter(user=request.user, is_archived=True)

    if request.method == "POST":
        if request.POST.get("button") == "restore":
            try:
                feedback = Feedback.objects.get(id=request.POST.get("restore_id"))
                feedback.is_archived = False
                feedback.is_viewed = False
                feedback.save()
                messages.success(request, 'Feedback Restored Successfully')
                return redirect('feedbacks_archive')
            except Exception as e:
                messages.error(request, 'Feedback Restoration Failed')
                print(e)
                return redirect('feedbacks_archive')
        elif request.POST.get("button") == "delete":
            try:
                feedback = Feedback.objects.get(id=request.POST.get("delete_id"))
                feedback.delete()
                messages.success(request, 'Feedback Deleted Successfully')
                return redirect('feedbacks_archive')
            except Exception as e:
                messages.error(request, 'Feedback Deletion Failed')
                print(e)
                return redirect('feedbacks_archive')



    return render(request, 'dashboard/feedbacks_archive.html',{
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),
        'feedbacks': feedbacks,
    })

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users = User.objects.filter(is_active=True)

    form = UserForm()

    if request.method == "POST":
        if "button" in request.POST:
            if request.POST.get("button") == "add":
                form = UserForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password("@default123")

                    role = request.POST.get("role")
                    if role == "admin":
                        user.is_superuser = True
                        user.is_staff = True
                    elif role == "owner":
                        user.is_superuser = False
                        user.is_staff = True
                    elif role == "tenant":
                        user.is_superuser = False
                        user.is_staff = False
                    user.save()
                    messages.success(request, 'User Added Successfully')
                    return redirect('users')
                else:
                    messages.error(request, 'User Addition Failed')
                    print(form.errors)
                    return redirect('users')
            elif request.POST.get("button") == "delete":
                try:
                    user = User.objects.get(id=request.POST.get("delete_id"))
                    user.is_active = False
                    user.save()
                    messages.success(request, 'User Deleted Successfully')
                    return redirect('users')
                except Exception as e:
                    messages.error(request, 'User Deletion Failed')
                    print(e)
                    return redirect('users')
            elif request.POST.get("button") == "edit":
                try:
                    user = User.objects.get(id=request.POST.get("edit_id"))
                    user.first_name = request.POST.get("edit_first_name")
                    user.last_name = request.POST.get("edit_last_name")
                    user.email = request.POST.get("edit_email")
                    user.username = request.POST.get("edit_username")
                    role = request.POST.get("edit_role")
                    if role == "admin":
                        user.is_superuser = True
                        user.is_staff = True
                    elif role == "owner":
                        user.is_superuser = False
                        user.is_staff = True
                    elif role == "tenant":
                        user.is_superuser = False
                        user.is_staff = False

                    user.save()
                    messages.success(request, 'User Updated Successfully')
                    return redirect('users')
                except Exception as e:
                    messages.error(request, 'User Update Failed')
                    print(e)
                    return redirect('users')

    return render(request,'dashboard/users.html', {
        'users': users,
        'form': form,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),

    })


@user_passes_test(lambda u: u.is_superuser)
def users_archive(request):
    users = User.objects.filter(is_active=False)

    if request.method == "POST":
        if request.POST.get("button") == "restore":
            try:
                user = User.objects.get(id=request.POST.get("restore_id"))
                user.is_active = True
                user.save()
                messages.success(request, 'User Restored Successfully')
                return redirect('users_archive')
            except Exception as e:
                messages.error(request, 'User Restoration Failed')
                print(e)
                return redirect('users_archive')
        elif request.POST.get("button") == "delete":
            try:
                user = User.objects.get(id=request.POST.get("delete_id"))
                user.delete()
                messages.success(request, 'User Deleted Successfully')
                return redirect('users_archive')
            except Exception as e:
                messages.error(request, 'User Deletion Failed')
                print(e)
                return redirect('users_archive')

    return render(request, 'dashboard/users_archive.html',{
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),
        'users': users,
    })




def landing_page(request):
    boardinghouses = BoardingHouse.objects.all()
    return render(request, 'landing_page/landing_page.html',{
        'boardinghouses': boardinghouses,
    })


def bhouse_listings(request):
    boardinghouses = BoardingHouse.objects.all()

    return render(request, 'landing_page/bhouse_listings.html',{
        'boardinghouses': boardinghouses,
    })


def bhouse_listings_detail(request, id):
    bhouse = get_object_or_404(BoardingHouse, id=id)
    rooms = Room.objects.filter(boardinghouse=bhouse)


    return render(request, 'landing_page/bhouse_listings_detail.html',{
        'bhouse': bhouse,
        'rooms': rooms,
    })


def room_listings(request):
    rooms = Room.objects.all()

    return render(request, 'landing_page/room_listings.html',{
        'rooms': rooms,
    })


def room_listings_detail(request, id):
    room = get_object_or_404(Room, id=id)
    bhouse = BoardingHouse.objects.get(id=room.boardinghouse.id)
    return render(request, 'landing_page/room_listings_detail.html',{
        'room': room,
        'bhouse': bhouse,
    })
