from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from homepage.forms import FeedbackForms
from homepage.models import Feedback


# Create your views here.
@login_required(login_url='login')
def homepage(request):
    if request.user.is_superuser:
        return redirect('dashboard')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def notice(request):
    return render(request, 'dashboard/notice.html')


def feedbacks(request):
    feedbacks = Feedback.objects.filter(user=request.user)

    if request.method == "POST":
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
    else:
        form = FeedbackForms()

    return render(request, 'dashboard/feedbacks.html',{
        'feedbacks': feedbacks,
        'form': form,
    })