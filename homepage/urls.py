from django.urls import path

from homepage import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notice/', views.notice, name='notice'),
    path('feedbacks/', views.feedbacks, name='feedbacks'),

]
