from django.urls import path

from boardinghouse import views

urlpatterns = [
    path('boardinghouse/', views.boardinghouse, name='boardinghouse'),
    path('boardinghouse/archive/', views.boardinghouse_archive, name='boardinghouse_archive'),
    path('boardinghouse/<int:id>/', views.boardinghouse_detail, name='boardinghouse_detail'),
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/archive/', views.rooms_archive, name='rooms_archive'),
    path('rooms/<int:id>/', views.rooms_detail, name='room_detail'),
    path('rooms/manage/', views.manage_rooms, name='manage_rooms'),
    path('rooms/manage/<int:id>/', views.manage_rooms_detail, name='manage_rooms_detail'),
    path('beds/', views.beds, name='beds'),
    path('beds_assignment/', views.beds_assignment, name='beds_assignment'),
]