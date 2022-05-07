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
    path('appDetail/<int:app_id>/<int:user_id>/', views.appDetail, name='appDetail'),
    path('removeApp/<int:app_id>/', views.removeApp, name='removeApp'),
    path('removeUser/<int:user_id>/', views.removeUser, name='removeUser'),
    path('removeDev/<int:dev_id>/', views.removeDev, name='removeDev'),
    path('appDetail/<int:app_id>/<int:user_id>/installApp/', views.installApp, name='installApp'),
    path('adminPage/<int:user_id>/newCategory/', views.newCategory, name='newCategory'),
    path('devPage/<int:user_id>/<int:app_id>/updateApp/', views.updateApp, name='updateApp'),
    path('userPage/<int:user_id>/manageAccount/', views.manageAccount, name='manageAccount'),
    path('devPage/<int:user_id>/manageAccount/', views.manageAccount, name='manageAccount'),
    path('devPage/<int:user_id>/<int:app_id>/removeApp', views.devRemoveApp, name='removeApp'),
    path('media/<path:path>', views.media, name='media'),
]