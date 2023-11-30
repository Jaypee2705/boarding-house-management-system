from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from homepage.forms import FeedbackForms, NoticeForms, UserForm
from homepage.models import Feedback, Notice


# Create your views here.
@login_required(login_url='login')
def homepage(request):
    if request.user.is_superuser:
        return redirect('dashboard')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def notice(request):
    notices = Notice.objects.filter(boardinghouse__owner=request.user)

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
                    notice.delete()
                    messages.success(request, 'Notice Deleted Successfully')
                    return redirect('notice')
                except Exception as e:
                    messages.error(request, 'Notice Deletion Failed')
                    print(e)
                    return redirect('notice')
    else:
        form = NoticeForms()


    return render(request, 'dashboard/notice.html',{
        'notices': notices,
        'form': form,

    })




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
    })


def feedbacks(request):
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
    })


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
    })


def user_detail(request):
    return None