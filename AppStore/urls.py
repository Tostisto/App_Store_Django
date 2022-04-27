from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('userPage/<int:user_id>/', views.userPage, name='userPage'),
    path('adminPage/', views.adminPage, name='adminPage'),
    path('devPage/<int:user_id>/', views.devPage, name='devPage'),
    path('devPage/<int:user_id>/newApp/', views.newApp, name='newApp'),
]