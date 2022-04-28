from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('devRegister/', views.devRegister, name='devRegister'),    
    path('userPage/<int:user_id>/', views.userPage, name='userPage'),
    path('adminPage/<int:user_id>/', views.adminPage, name='adminPage'),
    path('devPage/<int:user_id>/', views.devPage, name='devPage'),
    path('devPage/<int:user_id>/newApp/', views.newApp, name='newApp'),

    path('appDetail/<int:app_id>/', views.appDetail, name='appDetail')
]