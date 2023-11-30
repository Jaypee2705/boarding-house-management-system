from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from homepage.forms import FeedbackForms, NoticeForms
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