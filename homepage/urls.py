from django.urls import path

from homepage import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('listings/bhouse/', views.bhouse_listings, name='bhouse_listings'),
    path('listings/bhouse/<int:id>/', views.bhouse_listings_detail, name='bhouse_detail_detail'),
    path('listings/room/', views.room_listings, name='room_listings'),
    path('listings/room/<int:id>/', views.room_listings_detail, name='room_listings_detail'),




    path('homepage/', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('users/<int:id>/', views.user_detail, name='user_detail'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:id>/', views.notice_detail, name='notice_detail'),
    path('feedbacks/', views.feedbacks, name='feedbacks'),

]
