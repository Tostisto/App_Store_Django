from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('devRegister/', views.devRegister, name='devRegister'),
    path('logout/', views.logout, name='login'), 

    path('userPage/', views.userPage, name='userPage'),
    path('userPage/manageAccount/', views.manageAccount, name='manageAccount'),
    path('userPage/downloadedApps/', views.downloadedApps, name='downloadedApps'),


    path('devPage', views.devPage, name='devPage'),
    path('devPage/newApp/', views.newApp, name='newApp'),
    path('devPage/<int:app_id>/updateApp/', views.updateApp, name='updateApp'),
    path('devPage/manageAccount/', views.manageAccountDev, name='manageAccount'),
    path('devPage/<int:app_id>/removeApp', views.devRemoveApp, name='removeApp'),

    path('adminPage', views.adminPage, name='adminPage'),
    path('adminPage/newCategory', views.newCategory, name='newCategory'),


    path('appDetail/<int:app_id>/', views.appDetail, name='appDetail'),
    path('removeApp/<int:app_id>/', views.removeApp, name='removeApp'),
    path('removeUser/<int:user_id>/', views.removeUser, name='removeUser'),
    path('removeDev/<int:dev_id>/', views.removeDev, name='removeDev'),
    path('installApp/<int:app_id>', views.installApp, name='installApp'),

    path('media/<path:path>', views.media, name='media'),
]