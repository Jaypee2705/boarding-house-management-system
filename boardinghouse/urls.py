from django.urls import path

from boardinghouse import views

urlpatterns = [
    path('boardinghouse/', views.boardinghouse, name='boardinghouse'),
]