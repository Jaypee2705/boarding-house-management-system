from django.urls import path

from boardinghouse import views

urlpatterns = [
    path('boardinghouse/', views.boardinghouse, name='boardinghouse'),
    path('boardinghouse/<int:id>/', views.boardinghouse_detail, name='boardinghouse_detail'),
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:id>/', views.rooms_detail, name='room_detail'),
    path('rooms/manage/', views.manage_rooms, name='manage_rooms'),
    path('beds/', views.beds, name='beds'),
    path('beds_assignment/', views.beds_assignment, name='beds_assignment'),
]