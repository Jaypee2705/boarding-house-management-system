from django.urls import path

from homepage import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),



    path('homepage/', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('users/<int:id>/', views.user_detail, name='user_detail'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:id>/', views.notice_detail, name='notice_detail'),
    path('feedbacks/', views.feedbacks, name='feedbacks'),

]
