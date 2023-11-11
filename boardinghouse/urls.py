from django.urls import path

from boardinghouse import views

urlpatterns = [
    path('boardinghouse/', views.boardinghouse, name='boardinghouse'),
    path('rooms/', views.rooms, name='rooms'),
    path('beds/', views.beds, name='beds'),
    path('beds_assignment/', views.beds_assignment, name='beds_assignment'),
]