from django.urls import path

from homepage import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:id>/', views.notice_detail, name='notice_detail'),
    path('feedbacks/', views.feedbacks, name='feedbacks'),

]
