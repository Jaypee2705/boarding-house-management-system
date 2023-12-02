from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from boardinghouse.models import BoardingHouse, Room
from homepage.forms import FeedbackForms, NoticeForms, UserForm
from homepage.models import Feedback, Notice
from tenants.models import Tenant


# Create your views here.
@login_required(login_url='login')
def homepage(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    elif request.user.is_staff:
        return redirect('dashboard')
    elif request.user.is_active:
        return redirect('dashboard')

@user_passes_test(lambda u: u.is_authenticated )
def dashboard(request):
    tenants = Tenant.objects.all()
    tenants_count = tenants.count()
    boardinghouses = BoardingHouse.objects.all()
    boardinghouses_count = boardinghouses.count()
    rooms = Room.objects.all()
    rooms_count = rooms.count()
    owner = User.objects.filter(is_superuser=False, is_staff=True).count()



    return render(request, 'dashboard/dashboard.html',{
        'tenants_count': tenants_count,
        'boardinghouses_count': boardinghouses_count,
        'rooms_count': rooms_count,
        'owner': owner,
        'feedback': Feedback.objects.filter(is_viewed=False).count(),
        'notice': Notice.objects.filter(is_viewed=False).count(),

    })

@user_passes_test(lambda u: u.is_authenticated)
def notice(request):

    if request.user.is_superuser or request.user.is_staff:
        notices = Notice.objects.filter(boardinghouse__owner=request.user, is_archived=False)
    else:
        user = User.objects.get(id=request.user.id)
        tenant_instance = Tenant.objects.get(name__id=user.id)
        notices = Notice.objects.filter(boardinghouse = tenant_instance.room.boardinghouse, is_archived=False)
        for noti in notices:
            noti.is_viewed = True
            noti.save()

    if request.method == "POST":
        form = NoticeForms(request.POST)
        if "button" in request.POST:
            if request.POST.get("button") == "add_notice":

                if form.is_valid():
                    notice = form.save(commit=False)
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

    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def notice_archive(request):
    if request.user.is_superuser or request.user.is_staff:
        notices = Notice.objects.filter(boardinghouse__owner=request.user, is_archived=True)
    else:
        user = User.objects.get(id=request.user.id)
        tenant_instance = Tenant.objects.get(name__id=user.id)
        notices = Notice.objects.filter(boardinghouse=tenant_instance.room.boardinghouse, is_archived=True)

    if request.method == "POST":
        if request.POST.get("button") == "recover":
            try:
                notice = Notice.objects.get(id=request.POST.get("recover_id"))
                notice.is_archived = False
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

    if request.user.is_superuser or request.user.is_staff:
        feedbacks = Feedback.objects.all()
        for feeds in feedbacks:
            feeds.is_viewed = True
            feeds.save()
    else:
        feedbacks = Feedback.objects.filter(user=request.user)

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
                    feedback.delete()
                    messages.success(request, 'Feedback Deleted Successfully')
                    return redirect('feedbacks')
                except Exception as e:
                    messages.error(request, 'Feedback Deletion Failed')
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
def users(request):
    users = User.objects.all()

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
                    elif role == "manager":
                        user.is_superuser = False
                        user.is_staff = True
                    else:
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
                    user.delete()
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
                    else:
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

@user_passes_test(lambda u: u.is_superuser )
def user_detail(request):
    return None


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